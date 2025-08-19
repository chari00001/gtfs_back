from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.agency_service import AgencyService
from app.schemas.agency import AgencyRead as AgencySchema, AgencyCreate, AgencyUpdate

router = APIRouter()


@router.get("/", response_model=List[AgencySchema], summary="List all agencies")
async def list_agencies(
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """Tüm agency'leri listele"""
    service = AgencyService(db)
    return service.get_all(snapshot_id=snapshot_id, skip=skip, limit=limit)


@router.get("/{agency_id}", response_model=AgencySchema, summary="Get agency by ID")
async def get_agency(
    agency_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """ID ile agency getir"""
    service = AgencyService(db)
    agency = service.get_by_id(agency_id, snapshot_id)
    
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    return agency


@router.post("/", response_model=AgencySchema, summary="Create new agency")
async def create_agency(
    agency: AgencyCreate,
    snapshot_id: UUID = Query(..., description="Snapshot ID"),
    db: Session = Depends(get_db)
):
    """Yeni agency oluştur"""
    service = AgencyService(db)
    return service.create(agency, snapshot_id)


@router.put("/{agency_id}", response_model=AgencySchema, summary="Update agency")
async def update_agency(
    agency_id: str,
    agency: AgencyUpdate,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Agency güncelle"""
    service = AgencyService(db)
    updated_agency = service.update(agency_id, agency, snapshot_id)
    
    if not updated_agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    return updated_agency


@router.delete("/{agency_id}", summary="Delete agency")
async def delete_agency(
    agency_id: str,
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Agency sil"""
    service = AgencyService(db)
    success = service.delete(agency_id, snapshot_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Agency not found")
    
    return {"message": "Agency deleted successfully"}


@router.get("/search/by-name", response_model=List[AgencySchema], summary="Search agencies by name")
async def search_agencies_by_name(
    name: str = Query(..., description="Agency name to search"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Agency adı ile ara"""
    service = AgencyService(db)
    agencies = service.search_agencies(name=name, snapshot_id=snapshot_id)
    return agencies


@router.get("/filter/by-timezone", response_model=List[AgencySchema], summary="Get agencies by timezone")
async def get_agencies_by_timezone(
    timezone: str = Query(..., description="Timezone"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """Zaman dilimine göre agency'leri getir"""
    service = AgencyService(db)
    return service.get_agencies_by_timezone(timezone, snapshot_id)


@router.get("/filter/with-contact", response_model=List[AgencySchema], summary="Get agencies with contact info")
async def get_agencies_with_contact(
    contact_type: str = Query(..., regex="^(phone|email)$", description="Contact type"),
    snapshot_id: Optional[UUID] = Query(None, description="Filter by snapshot ID"),
    db: Session = Depends(get_db)
):
    """İletişim bilgisi olan agency'leri getir"""
    service = AgencyService(db)
    
    if contact_type == "phone":
        return service.get_agencies_with_phone(snapshot_id)
    else:
        return service.get_agencies_with_email(snapshot_id)


@router.get("/snapshots/list", summary="List agency snapshots")
async def list_agency_snapshots(db: Session = Depends(get_db)):
    """Agency snapshot'larını listele"""
    service = AgencyService(db)
    return service.get_snapshots()
