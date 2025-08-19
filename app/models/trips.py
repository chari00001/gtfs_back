from __future__ import annotations

from sqlalchemy import Column, String, SmallInteger, ForeignKey, UniqueConstraint

from app.models.base import GTFSBase


class Trips(GTFSBase):
    __tablename__ = "trips"

    trip_id = Column(String, primary_key=True)
    route_id = Column(String, ForeignKey("routes.route_id"))
    service_id = Column(String, ForeignKey("calendar.service_id"))
    trip_headsign = Column(String)
    direction_id = Column(SmallInteger)
    block_id = Column(String)
    shape_id = Column(String)  # References shapes.shape_id but no FK constraint due to composite PK

    __table_args__ = (
        UniqueConstraint('trip_id', 'snapshot_id', name='uq_trips_snapshot'),
    )
