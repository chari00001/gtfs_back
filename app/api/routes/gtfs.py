from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.gtfs_upload import GTFSUploadService

router = APIRouter()
logger = logging.getLogger(__name__)

# Upload durumlarını takip etmek için in-memory store
upload_statuses: Dict[str, Dict[str, Any]] = {}


@router.post("/upload", summary="Upload GTFS ZIP file")
async def upload_gtfs_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="GTFS ZIP file containing 11 txt files"),
    db: Session = Depends(get_db)
):
    # Dosya türü kontrolü
    if not file.filename or not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a ZIP file")
    
    try:
        # Upload service'i oluştur
        upload_service = GTFSUploadService(db)
        snapshot_id = upload_service.snapshot_id
        
        # Upload durumunu kaydet
        upload_statuses[snapshot_id] = upload_service.get_upload_status()
        
        logger.info(f"Starting GTFS upload for file: {file.filename}, snapshot: {snapshot_id}")
        
        # Dosya içeriğini oku
        file_content = await file.read()
        
        # Background task olarak işle (DB session geçirme - thread-safe)
        background_tasks.add_task(
            process_gtfs_upload,
            file_content,
            snapshot_id
        )
        
        return {
            "message": "GTFS upload started successfully",
            "snapshot_id": snapshot_id,
            "status_url": f"/api/gtfs/upload/{snapshot_id}/status"
        }
        
    except Exception as e:
        logger.error(f"Error starting GTFS upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting upload: {str(e)}")


@router.get("/upload/{snapshot_id}/status", summary="Get upload status")
async def get_upload_status(snapshot_id: str):
    """Upload durumunu sorgula"""
    
    if snapshot_id not in upload_statuses:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    return upload_statuses[snapshot_id]


@router.get("/snapshots", summary="List all snapshots")
async def list_snapshots(db: Session = Depends(get_db)):
    """Tüm snapshot'ları listele"""
    
    try:
        # Agency tablosundan unique snapshot'ları al (örnek olarak)
        from app.models.agency import Agency
        from sqlalchemy import distinct, desc
        
        snapshots = db.query(
            distinct(Agency.snapshot_id).label('snapshot_id'),
            Agency.created_at
        ).order_by(desc(Agency.created_at)).all()
        
        return {
            "snapshots": [
                {
                    "snapshot_id": s.snapshot_id,
                    "created_at": s.created_at.isoformat()
                }
                for s in snapshots
            ]
        }
        
    except Exception as e:
        logger.error(f"Error listing snapshots: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing snapshots")


@router.delete("/snapshots/{snapshot_id}", summary="Delete a snapshot")
async def delete_snapshot(snapshot_id: str, db: Session = Depends(get_db)):
    """Snapshot'ı cascade delete ile sil"""
    
    try:
        # Tüm tablolardan bu snapshot_id'ye sahip kayıtları sil
        from app.services.gtfs_upload import GTFSUploadService
        
        logger.info(f"Snapshot {snapshot_id} silme işlemi başlatılıyor...")
        
        deleted_count = 0
        # Ters sırada sil (foreign key bağımlılıkları nedeniyle)
        for model_class in reversed(list(GTFSUploadService.GTFS_FILES_MAPPING.values())):
            logger.debug(f"Tablo {model_class.__tablename__} için snapshot {snapshot_id} kayıtları siliniyor...")
            
            # Önce kaç kayıt var kontrol et
            count_before = db.query(model_class).filter(
                model_class.snapshot_id == snapshot_id
            ).count()
            
            logger.debug(f"Tablo {model_class.__tablename__}'da {count_before} kayıt bulundu")
            
            result = db.query(model_class).filter(
                model_class.snapshot_id == snapshot_id
            ).delete(synchronize_session=False)
            
            deleted_count += result
            logger.debug(f"Tablo {model_class.__tablename__}'dan {result} kayıt silindi")
        
        logger.info(f"Toplam {deleted_count} kayıt silindi")
        
        if deleted_count == 0:
            logger.warning(f"Snapshot {snapshot_id} için hiç kayıt bulunamadı")
            raise HTTPException(status_code=404, detail="Snapshot bulunamadı")
        
        db.commit()
        logger.info(f"Veritabanı değişiklikleri commit edildi")
        
        # Upload status'u da temizle
        if snapshot_id in upload_statuses:
            del upload_statuses[snapshot_id]
            logger.debug(f"Upload status temizlendi")
        
        logger.info(f"Snapshot {snapshot_id} silindi, {deleted_count} kayıt kaldırıldı")
        
        return {
            "message": f"Snapshot {snapshot_id} başarıyla silindi",
            "deleted_records": deleted_count
        }
        
    except HTTPException:
        logger.error(f"HTTP Exception: Snapshot {snapshot_id} bulunamadı")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Snapshot {snapshot_id} silinirken beklenmeyen hata: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Snapshot silinirken hata oluştu: {str(e)}")


@router.post("/cleanup", summary="Cleanup old snapshots")
async def cleanup_snapshots(
    keep_count: int = 5,
    db: Session = Depends(get_db)
):
    """Eski snapshot'ları temizle"""
    
    try:
        await GTFSUploadService.cleanup_old_snapshots(db, keep_count)
        
        return {
            "message": f"Cleanup completed, kept latest {keep_count} snapshots"
        }
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during cleanup")


async def process_gtfs_upload(
    file_content: bytes,
    snapshot_id: str
):
    """Background task olarak GTFS upload'ını işle - Thread-safe DB session ile"""
    
    # Background task'ta YENİ DB SESSION oluştur (thread-safe)
    from app.db.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Yeni session ile upload service oluştur
        upload_service = GTFSUploadService(db)
        upload_service.snapshot_id = snapshot_id  # Mevcut snapshot_id'yi kullan
        
        # Upload'ı işle
        result = await upload_service.process_gtfs_zip(file_content)
        
        # Durumu güncelle
        upload_statuses[snapshot_id] = result
        
        logger.info(f"GTFS upload completed for snapshot {snapshot_id}: {result['status']}")
        
    except Exception as e:
        logger.error(f"Error in background GTFS upload {snapshot_id}: {str(e)}")
        
        # Hata durumunu kaydet
        upload_statuses[snapshot_id] = {
            'snapshot_id': snapshot_id,
            'status': 'failed',
            'total_files': 0,
            'processed_files': 0,
            'errors': [str(e)],
            'started_at': datetime.utcnow(),
            'completed_at': datetime.utcnow(),
        }
        
    finally:
        # Session'ı mutlaka kapat
        db.close()
        logger.info(f"Database session closed for snapshot {snapshot_id}")
