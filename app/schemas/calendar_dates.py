from __future__ import annotations

from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CalendarDatesBase(BaseModel):
    date: date
    exception_type: int


class CalendarDatesCreate(CalendarDatesBase):
    service_id: str


class CalendarDatesRead(CalendarDatesBase):
    model_config = ConfigDict(from_attributes=True)
    
    service_id: str


class CalendarDatesUpdate(BaseModel):
    date: Optional[date] = None
    exception_type: Optional[int] = None
