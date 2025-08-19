from __future__ import annotations

from sqlalchemy import Column, String, Integer, Float, PrimaryKeyConstraint, UniqueConstraint

from app.models.base import GTFSBase


class Shapes(GTFSBase):
    __tablename__ = "shapes"

    shape_id = Column(String, nullable=False)
    shape_pt_lat = Column(Float, nullable=False)
    shape_pt_lon = Column(Float, nullable=False)
    shape_pt_sequence = Column(Integer, nullable=False)
    shape_dist_traveled = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('shape_id', 'shape_pt_sequence'),
        UniqueConstraint('shape_id', 'shape_pt_sequence', 'snapshot_id', name='uq_shapes_snapshot'),
    )
