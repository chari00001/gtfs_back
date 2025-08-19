from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class FareAttributesBase(BaseModel):
    agency_id: str | None = None
    price: Decimal | None = None
    currency_type: str | None = None
    payment_method: int | None = None
    transfers: int | None = None
    transfer_duration: int | None = None


class FareAttributesCreate(FareAttributesBase):
    fare_id: str


class FareAttributesRead(FareAttributesBase):
    model_config = ConfigDict(from_attributes=True)
    
    fare_id: str


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


class FareAttributesUpdate(BaseModel):
    agency_id: str | None = None
    price: Decimal | None = None
    currency_type: str | None = None
    payment_method: int | None = None
    transfers: int | None = None
    transfer_duration: int | None = None


class FareRulesUpdate(BaseModel):
    origin_id: str | None = None
    destination_id: str | None = None
    contains_id: str | None = None
