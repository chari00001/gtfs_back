from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FareRulesBase(BaseModel):
    origin_id: str | None = None
    destination_id: str | None = None
    contains_id: str | None = None


class FareRulesCreate(FareRulesBase):
    fare_id: str
    route_id: str


class FareRulesRead(FareRulesBase):
    model_config = ConfigDict(from_attributes=True)
    
    fare_id: str
    route_id: str


class FareRulesUpdate(BaseModel):
    origin_id: str | None = None
    destination_id: str | None = None
    contains_id: str | None = None
