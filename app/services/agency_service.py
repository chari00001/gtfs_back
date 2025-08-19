from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.agency import Agency
from app.schemas.agency import AgencyCreate, AgencyUpdate
from app.services.base_service import BaseService


class AgencyService(BaseService[Agency, AgencyCreate, AgencyUpdate]):
    """Agency tablosu için özel servis"""
    
    def __init__(self, db: Session):
        super().__init__(Agency, db)
    
    # AGENCY-SPESİFİK OPERASYONLAR
    
    def get_by_name(self, agency_name: str, snapshot_id: Optional[UUID] = None) -> Optional[Agency]:
        """Agency adı ile ara"""
        query = self.db.query(Agency).filter(Agency.agency_name.ilike(f"%{agency_name}%"))
        
        if snapshot_id:
            query = query.filter(Agency.snapshot_id == snapshot_id)
        
        return query.first()
    
    def get_agencies_by_timezone(self, timezone: str, snapshot_id: Optional[UUID] = None) -> List[Agency]:
        """Zaman dilimi ile agency'leri getir"""
        query = self.db.query(Agency).filter(Agency.agency_timezone == timezone)
        
        if snapshot_id:
            query = query.filter(Agency.snapshot_id == snapshot_id)
        
        return query.all()
    
    def get_agencies_with_phone(self, snapshot_id: Optional[UUID] = None) -> List[Agency]:
        """Telefonu olan agency'leri getir"""
        query = self.db.query(Agency).filter(Agency.agency_phone.isnot(None))
        
        if snapshot_id:
            query = query.filter(Agency.snapshot_id == snapshot_id)
        
        return query.all()
    
    def get_agencies_with_email(self, snapshot_id: Optional[UUID] = None) -> List[Agency]:
        """Email'i olan agency'leri getir"""
        query = self.db.query(Agency).filter(Agency.agency_email.isnot(None))
        
        if snapshot_id:
            query = query.filter(Agency.snapshot_id == snapshot_id)
        
        return query.all()
    
    def search_agencies(
        self, 
        name: Optional[str] = None,
        timezone: Optional[str] = None,
        has_phone: Optional[bool] = None,
        has_email: Optional[bool] = None,
        snapshot_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agency]:
        """Gelişmiş agency arama"""
        query = self.db.query(Agency)
        
        if name:
            query = query.filter(Agency.agency_name.ilike(f"%{name}%"))
        
        if timezone:
            query = query.filter(Agency.agency_timezone == timezone)
        
        if has_phone is not None:
            if has_phone:
                query = query.filter(Agency.agency_phone.isnot(None))
            else:
                query = query.filter(Agency.agency_phone.is_(None))
        
        if has_email is not None:
            if has_email:
                query = query.filter(Agency.agency_email.isnot(None))
            else:
                query = query.filter(Agency.agency_email.is_(None))
        
        if snapshot_id:
            query = query.filter(Agency.snapshot_id == snapshot_id)
        
        return query.offset(skip).limit(limit).all()
