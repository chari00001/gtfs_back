from __future__ import annotations

import asyncio
import csv
import io
import logging
import uuid
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import OrderedDict
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import (
    Agency, Routes, Stops, Trips, StopTimes, Calendar, CalendarDates,
    Shapes, FareAttributes, FareRules, FeedInfo
)

logger = logging.getLogger(__name__)


class GTFSUploadService:
    """GTFS dosya yükleme ve işleme servisi"""
    
    # GTFS dosya adları ve karşılık gelen model sınıfları
    GTFS_FILES_MAPPING = OrderedDict({
        'agency.txt': Agency,
        'calendar.txt': Calendar,
        'calendar_dates.txt': CalendarDates,
        'feed_info.txt': FeedInfo,
        'routes.txt': Routes,                   # ← ÖNCE routes
        'stops.txt': Stops,
        'shapes.txt': Shapes,
        'fare_attributes.txt': FareAttributes,  # ← fare_attributes önce
        'fare_rules.txt': FareRules,            # ← fare_rules sonra (routes'a bağımlı)
        'trips.txt': Trips,                     # ← trips (routes'a bağımlı)
        'stop_times.txt': StopTimes,            # ← stop_times (trips'e bağımlı)
    })

    def __init__(self, db: Session):
        self.db = db
        self.snapshot_id = str(uuid.uuid4())
        self.upload_status = {
            'snapshot_id': self.snapshot_id,
            'status': 'pending',
            'total_files': 0,
            'processed_files': 0,
            'errors': [],
            'started_at': datetime.utcnow(),
            'completed_at': None,
        }

    async def process_gtfs_zip(self, zip_content: bytes) -> Dict[str, Any]:
        """ZIP dosyasını işle ve veritabanına yükle"""
        try:
            self.upload_status['status'] = 'processing'
            
            # ZIP dosyasını aç
            with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_file:
                file_list = zip_file.namelist()
                gtfs_files = [f for f in file_list if f in self.GTFS_FILES_MAPPING]
                
                self.upload_status['total_files'] = len(gtfs_files)
                logger.info(f"Processing {len(gtfs_files)} GTFS files for snapshot {self.snapshot_id}")

                # Her dosyayı işle - DOĞRU SIRA (GTFS_FILES_MAPPING sırasında)
                for filename in self.GTFS_FILES_MAPPING.keys():
                    if filename in gtfs_files:
                        try:
                            await self._process_single_file(zip_file, filename)
                            self.upload_status['processed_files'] += 1
                            logger.info(f"Processed {filename} ({self.upload_status['processed_files']}/{self.upload_status['total_files']})")
                        except Exception as e:
                            logger.error(f"Error processing {filename}: {e}")
                            self.upload_status['errors'].append(f"{filename}: {str(e)}")

            # Tamamlandı durumunu güncelle
            self.upload_status['status'] = 'completed' if not self.upload_status['errors'] else 'completed_with_errors'
            self.upload_status['completed_at'] = datetime.utcnow()
            
            # Commit transaction
            self.db.commit()
            
            logger.info(f"GTFS upload completed for snapshot {self.snapshot_id}")
            return self.upload_status

        except Exception as e:
            self.upload_status['status'] = 'failed'
            self.upload_status['errors'].append(f"Fatal error: {str(e)}")
            self.upload_status['completed_at'] = datetime.utcnow()
            
            # Rollback on error
            self.db.rollback()
            
            logger.error(f"GTFS upload failed for snapshot {self.snapshot_id}: {str(e)}")
            return self.upload_status

    async def _process_single_file(self, zip_file: zipfile.ZipFile, filename: str) -> None:
        """Tek bir GTFS dosyasını işle"""
        model_class = self.GTFS_FILES_MAPPING[filename]
        
        # Dosya içeriğini oku
        with zip_file.open(filename) as file:
            content = file.read().decode('utf-8')
        
        # CSV olarak parse et
        csv_reader = csv.DictReader(io.StringIO(content))
        
        # Batch insert için verileri hazırla
        batch_data = []
        batch_size = 500  # 1000'den 500'e düşür
        
        for row in csv_reader:
            # Snapshot ID ekle
            row['snapshot_id'] = self.snapshot_id
            row['created_at'] = datetime.utcnow()
            row['updated_at'] = datetime.utcnow()
            
            # Boş stringleri None'a çevir
            cleaned_row = {k: (v if v != '' else None) for k, v in row.items()}
            batch_data.append(cleaned_row)
            
            # Batch boyutuna ulaştığında veritabanına yaz
            if len(batch_data) >= batch_size:
                await self._bulk_insert(model_class, batch_data)
                batch_data = []
                
                # CPU'ya nefes aldır - EVENT LOOP'A CONTROL VER
                await asyncio.sleep(0.001)  # 1ms yield
        
        # Kalan verileri yaz
        if batch_data:
            await self._bulk_insert(model_class, batch_data)

    async def _bulk_insert(self, model_class, data: List[Dict[str, Any]]) -> None:
        """Bulk insert işlemi - Non-blocking"""
        if not data:
            return
            
        try:
            # SQLAlchemy Core kullanarak bulk insert
            table = model_class.__table__
            
            # Blocking operation'ı thread pool'da çalıştır
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,  # Default thread pool
                lambda: self.db.execute(table.insert(), data)
            )
            
            # Event loop'a control ver
            await asyncio.sleep(0)
            
        except Exception as e:
            logger.error(f"Bulk insert error for {model_class.__name__}: {str(e)}")
            raise

    def get_upload_status(self) -> Dict[str, Any]:
        """Upload durumunu döndür"""
        return self.upload_status

    @classmethod
    async def cleanup_old_snapshots(cls, db: Session, keep_count: int = 5) -> None:
        """Eski snapshot'ları temizle"""
        try:
            # Her tablo için eski snapshot'ları sil
            for model_class in cls.GTFS_FILES_MAPPING.values():
                table_name = model_class.__tablename__
                
                # En son keep_count kadar snapshot'ı tut
                cleanup_query = text(f"""
                    DELETE FROM {table_name} 
                    WHERE snapshot_id NOT IN (
                        SELECT DISTINCT snapshot_id 
                        FROM {table_name} 
                        ORDER BY created_at DESC 
                        LIMIT :keep_count
                    )
                """)
                
                db.execute(cleanup_query, {'keep_count': keep_count})
            
            db.commit()
            logger.info(f"Cleaned up old snapshots, kept latest {keep_count}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error cleaning up snapshots: {str(e)}")
            raise
