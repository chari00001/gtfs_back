from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TripsBase(BaseModel):
    route_id: str | None = None
    service_id: str | None = None
    trip_headsign: str | None = None
    direction_id: int | None = None
    block_id: str | None = None
    shape_id: str | None = None


class TripsCreate(TripsBase):
    trip_id: str


class TripsRead(TripsBase):
    model_config = ConfigDict(from_attributes=True)
    
    trip_id: str


class TripsUpdate(TripsBase):
    pass
