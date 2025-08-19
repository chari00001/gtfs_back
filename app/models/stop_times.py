from __future__ import annotations

from sqlalchemy import Column, String, Integer, SmallInteger, Float, Time, ForeignKey, UniqueConstraint

from app.models.base import GTFSBase


class StopTimes(GTFSBase):
    __tablename__ = "stop_times"

    trip_id = Column(String, ForeignKey("trips.trip_id"), primary_key=True)
    stop_sequence = Column(Integer, primary_key=True)
    arrival_time = Column(Time)
    departure_time = Column(Time)
    stop_id = Column(String, ForeignKey("stops.stop_id"))
    stop_headsign = Column(String)
    pickup_type = Column(SmallInteger)
    drop_off_type = Column(SmallInteger)
    shape_dist_traveled = Column(Float)

    __table_args__ = (
        UniqueConstraint('trip_id', 'stop_sequence', 'snapshot_id', name='uq_stop_times_snapshot'),
    )
