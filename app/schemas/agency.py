from __future__ import annotations

from pydantic import BaseModel, ConfigDict

class AgencyBase(BaseModel):
    agency_name: str
    agency_url: str
    agency_timezone: str
    agency_lang: str | None = None
    agency_phone: str | None = None
    agency_fare_url: str | None = None
    agency_email: str | None = None


class AgencyCreate(AgencyBase):
    agency_id: str


class AgencyRead(AgencyBase):
    model_config = ConfigDict(from_attributes=True)
    
    agency_id: str


class AgencyUpdate(BaseModel):
    agency_name: str | None = None
    agency_url: str | None = None
    agency_timezone: str | None = None
    agency_lang: str | None = None
    agency_phone: str | None = None
    agency_fare_url: str | None = None
    agency_email: str | None = None
