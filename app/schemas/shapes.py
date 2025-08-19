from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ShapesBase(BaseModel):
    shape_pt_lat: float
    shape_pt_lon: float
    shape_dist_traveled: float | None = None


class ShapesCreate(ShapesBase):
    shape_id: str
    shape_pt_sequence: int


class ShapesRead(ShapesBase):
    model_config = ConfigDict(from_attributes=True)
    
    shape_id: str
    shape_pt_sequence: int


class ShapesUpdate(BaseModel):
    shape_pt_lat: float | None = None
    shape_pt_lon: float | None = None
    shape_dist_traveled: float | None = None
