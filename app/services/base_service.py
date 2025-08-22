from __future__ import annotations

from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from pydantic import BaseModel

from app.models.base import GTFSBase

ModelType = TypeVar("ModelType", bound=GTFSBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Tüm GTFS servisleri için temel CRUD operasyonları"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    # TEMEL CRUD OPERASYONLARI
    
    def get_all(
        self, 
        snapshot_id: Optional[UUID] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """Tüm kayıtları getir"""
        query = self.db.query(self.model)
        
        if snapshot_id:
            query = query.filter(self.model.snapshot_id == str(snapshot_id))
        
        return query.order_by(desc(self.model.created_at)).offset(skip).limit(limit).all()
    
    def get_by_id(self, record_id: str, snapshot_id: Optional[UUID] = None) -> Optional[ModelType]:
        """ID ile kayıt getir"""
        pk_column = self.model.get_primary_key_column()
        query = self.db.query(self.model).filter(pk_column == record_id)
        
        if snapshot_id:
            query = query.filter(self.model.snapshot_id == str(snapshot_id))
        
        return query.first()
    
    def create(self, obj_in: CreateSchemaType, snapshot_id: UUID) -> ModelType:
        """Yeni kayıt oluştur"""
        obj_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
        obj_data['snapshot_id'] = str(snapshot_id)
        
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        record_id: str, 
        obj_in: UpdateSchemaType,
        snapshot_id: Optional[UUID] = None
    ) -> Optional[ModelType]:
        """Kayıt güncelle"""
        db_obj = self.get_by_id(record_id, snapshot_id)
        if not db_obj:
            return None
        
        obj_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, 'model_dump') else obj_in.dict(exclude_unset=True)
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, record_id: str, snapshot_id: Optional[UUID] = None) -> bool:
        """Kayıt sil"""
        db_obj = self.get_by_id(record_id, snapshot_id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def get_count(self, snapshot_id: Optional[UUID] = None) -> int:
        """Toplam kayıt sayısı"""
        query = self.db.query(self.model)
        
        if snapshot_id:
            query = query.filter(self.model.snapshot_id == str(snapshot_id))
        
        return query.count()
    
    # SNAPSHOT İŞLEMLERİ
    
    def get_snapshots(self) -> List[Dict[str, Any]]:
        """Tüm snapshot'ları listele"""
        from sqlalchemy import distinct
        
        snapshots = self.db.query(
            distinct(self.model.snapshot_id).label('snapshot_id'),
            self.model.created_at
        ).order_by(desc(self.model.created_at)).all()
        
        return [
            {
                "snapshot_id": str(s.snapshot_id),
                "created_at": s.created_at.isoformat(),
                "record_count": self.get_count(s.snapshot_id)
            }
            for s in snapshots
        ]
    
    def delete_snapshot(self, snapshot_id: UUID) -> int:
        """Snapshot'taki tüm kayıtları sil"""
        deleted_count = self.db.query(self.model).filter(
            self.model.snapshot_id == str(snapshot_id)
        ).delete()
        
        self.db.commit()
        return deleted_count
    
    # BULK OPERASYONLAR
    
    def bulk_create(self, objs_in: List[CreateSchemaType], snapshot_id: UUID) -> List[ModelType]:
        """Toplu kayıt oluştur"""
        db_objs = []
        
        for obj_in in objs_in:
            obj_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
            obj_data['snapshot_id'] = str(snapshot_id)
            db_objs.append(self.model(**obj_data))
        
        self.db.add_all(db_objs)
        self.db.commit()
        
        for db_obj in db_objs:
            self.db.refresh(db_obj)
        
        return db_objs
    
    def bulk_delete(self, record_ids: List[str], snapshot_id: Optional[UUID] = None) -> int:
        """Toplu kayıt sil"""
        pk_column = self.model.get_primary_key_column()
        query = self.db.query(self.model).filter(pk_column.in_(record_ids))
        
        if snapshot_id:
            query = query.filter(self.model.snapshot_id == str(snapshot_id))
        
        deleted_count = query.delete(synchronize_session=False)
        self.db.commit()
        return deleted_count
