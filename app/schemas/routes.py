from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RoutesBase(BaseModel):
    agency_id: str | None = None
    route_short_name: str | None = None
    route_long_name: str | None = None
    route_desc: str | None = None
    route_type: int
    route_url: str | None = None
    route_color: str | None = None
    route_text_color: str | None = None


class RoutesCreate(RoutesBase):
    route_id: str


class RoutesRead(RoutesBase):
    model_config = ConfigDict(from_attributes=True)
    
    route_id: str


class RoutesUpdate(BaseModel):
    agency_id: str | None = None
    route_short_name: str | None = None
    route_long_name: str | None = None
    route_desc: str | None = None
    route_type: int | None = None
    route_url: str | None = None
    route_color: str | None = None
    route_text_color: str | None = None
