from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class StopsBase(BaseModel):
    stop_name: str
    stop_desc: str | None = None
    stop_lat: float
    stop_lon: float
    zone_id: str | None = None
    stop_url: str | None = None


class StopsCreate(StopsBase):
    stop_id: str


class StopsRead(StopsBase):
    model_config = ConfigDict(from_attributes=True)
    
    stop_id: str


class StopsUpdate(BaseModel):
    stop_name: str | None = None
    stop_desc: str | None = None
    stop_lat: float | None = None
    stop_lon: float | None = None
    zone_id: str | None = None
    stop_url: str | None = None
