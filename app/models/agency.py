from __future__ import annotations

from sqlalchemy import Column, String, UniqueConstraint

from app.models.base import GTFSBase


class Agency(GTFSBase):
    __tablename__ = "agency"

    agency_id = Column(String, primary_key=True)
    agency_name = Column(String, nullable=False)
    agency_url = Column(String, nullable=False)
    agency_timezone = Column(String, nullable=False)
    agency_lang = Column(String)
    agency_phone = Column(String)
    agency_fare_url = Column(String)
    agency_email = Column(String)

    __table_args__ = (
        UniqueConstraint('agency_id', 'snapshot_id', name='uq_agency_snapshot'),
    )
