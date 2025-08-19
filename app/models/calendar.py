from __future__ import annotations

from sqlalchemy import Column, String, SmallInteger, Date, ForeignKey, UniqueConstraint

from app.models.base import GTFSBase


class Calendar(GTFSBase):
    __tablename__ = "calendar"

    service_id = Column(String, primary_key=True)
    monday = Column(SmallInteger)
    tuesday = Column(SmallInteger)
    wednesday = Column(SmallInteger)
    thursday = Column(SmallInteger)
    friday = Column(SmallInteger)
    saturday = Column(SmallInteger)
    sunday = Column(SmallInteger)
    start_date = Column(Date)
    end_date = Column(Date)

    __table_args__ = (
        UniqueConstraint('service_id', 'snapshot_id', name='uq_calendar_snapshot'),
    )


class CalendarDates(GTFSBase):
    __tablename__ = "calendar_dates"

    service_id = Column(String, ForeignKey("calendar.service_id"), primary_key=True)
    date = Column(Date, primary_key=True)
    exception_type = Column(SmallInteger)

    __table_args__ = (
        UniqueConstraint('service_id', 'date', 'snapshot_id', name='uq_calendar_dates_snapshot'),
    )
