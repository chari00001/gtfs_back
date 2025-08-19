from __future__ import annotations

from datetime import time
from pydantic import BaseModel, ConfigDict


class StopTimesBase(BaseModel):
    arrival_time: time | None = None
    departure_time: time | None = None
    stop_id: str | None = None
    stop_headsign: str | None = None
    pickup_type: int | None = None
    drop_off_type: int | None = None
    shape_dist_traveled: float | None = None


class StopTimesCreate(StopTimesBase):
    trip_id: str
    stop_sequence: int


class StopTimesRead(StopTimesBase):
    model_config = ConfigDict(from_attributes=True)
    
    trip_id: str
    stop_sequence: int


class StopTimesUpdate(BaseModel):
    arrival_time: time | None = None
    departure_time: time | None = None
    stop_id: str | None = None
    stop_headsign: str | None = None
    pickup_type: int | None = None
    drop_off_type: int | None = None
    shape_dist_traveled: float | None = None
