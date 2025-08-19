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


class FareRules(GTFSBase):
    __tablename__ = "fare_rules"

    fare_id = Column(String, ForeignKey("fare_attributes.fare_id"), primary_key=True)
    route_id = Column(String, ForeignKey("routes.route_id"), primary_key=True)
    origin_id = Column(String)
    destination_id = Column(String)
    contains_id = Column(String)

    __table_args__ = (
        UniqueConstraint('fare_id', 'route_id', 'snapshot_id', name='uq_fare_rules_snapshot'),
    )
