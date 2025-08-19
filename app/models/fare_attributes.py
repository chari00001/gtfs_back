from __future__ import annotations

from sqlalchemy import Column, String, SmallInteger, Integer, Numeric, ForeignKey, UniqueConstraint

from app.models.base import GTFSBase


class FareAttributes(GTFSBase):
    __tablename__ = "fare_attributes"

    fare_id = Column(String, primary_key=True)
    agency_id = Column(String, ForeignKey("agency.agency_id"))
    price = Column(Numeric)
    currency_type = Column(String)
    payment_method = Column(SmallInteger)
    transfers = Column(SmallInteger)
    transfer_duration = Column(Integer)

    __table_args__ = (
        UniqueConstraint('fare_id', 'snapshot_id', name='uq_fare_attributes_snapshot'),
    )
