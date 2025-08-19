from __future__ import annotations

from datetime import date
from pydantic import BaseModel, ConfigDict


class FeedInfoBase(BaseModel):
    feed_publisher_name: str | None = None
    feed_publisher_url: str | None = None
    feed_lang: str | None = None
    feed_start_date: date | None = None
    feed_end_date: date | None = None
    feed_version: str | None = None
    feed_contact_email: str | None = None
    feed_contact_url: str | None = None


class FeedInfoCreate(FeedInfoBase):
    id: str = "default"


class FeedInfoRead(FeedInfoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str


class FeedInfoUpdate(FeedInfoBase):
    pass
