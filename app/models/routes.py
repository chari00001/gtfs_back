from __future__ import annotations

from sqlalchemy import Column, String, SmallInteger, ForeignKey, UniqueConstraint

from app.models.base import GTFSBase


class Routes(GTFSBase):
    __tablename__ = "routes"

    route_id = Column(String, primary_key=True)
    agency_id = Column(String, ForeignKey("agency.agency_id"))
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_desc = Column(String)
    route_type = Column(SmallInteger, nullable=False)
    route_url = Column(String)
    route_color = Column(String)
    route_text_color = Column(String)

    __table_args__ = (
        UniqueConstraint('route_id', 'snapshot_id', name='uq_routes_snapshot'),
    )
