from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StopTimesBase(BaseModel):
    arrival_time: str | None = None  # GTFS allows 24:xx:xx format
    departure_time: str | None = None  # GTFS allows 24:xx:xx format
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
    arrival_time: str | None = None  # GTFS allows 24:xx:xx format
    departure_time: str | None = None  # GTFS allows 24:xx:xx format
    stop_id: str | None = None
    stop_headsign: str | None = None
    pickup_type: int | None = None
    drop_off_type: int | None = None
    shape_dist_traveled: float | None = None
