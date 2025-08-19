from __future__ import annotations

from datetime import date
from pydantic import BaseModel, ConfigDict


class CalendarBase(BaseModel):
    monday: int | None = None
    tuesday: int | None = None
    wednesday: int | None = None
    thursday: int | None = None
    friday: int | None = None
    saturday: int | None = None
    sunday: int | None = None
    start_date: date | None = None
    end_date: date | None = None


class CalendarCreate(CalendarBase):
    service_id: str


class CalendarRead(CalendarBase):
    model_config = ConfigDict(from_attributes=True)
    
    service_id: str


class CalendarUpdate(CalendarBase):
    pass


class CalendarDatesBase(BaseModel):
    date: date
    exception_type: int


class CalendarDatesCreate(CalendarDatesBase):
    service_id: str


class CalendarDatesRead(CalendarDatesBase):
    model_config = ConfigDict(from_attributes=True)
    
    service_id: str
