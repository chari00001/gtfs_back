from __future__ import annotations

from sqlalchemy import Column, String, Float, UniqueConstraint

from app.models.base import GTFSBase


class Stops(GTFSBase):
    __tablename__ = "stops"

    stop_id = Column(String, primary_key=True)
    stop_name = Column(String, nullable=False)
    stop_desc = Column(String)
    stop_lat = Column(Float, nullable=False)
    stop_lon = Column(Float, nullable=False)
    zone_id = Column(String)
    stop_url = Column(String)

    __table_args__ = (
        UniqueConstraint('stop_id', 'snapshot_id', name='uq_stops_snapshot'),
    )
