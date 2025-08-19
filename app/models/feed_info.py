from __future__ import annotations

from sqlalchemy import Column, String, Date, UniqueConstraint

from app.models.base import GTFSBase


class FeedInfo(GTFSBase):
    __tablename__ = "feed_info"

    feed_publisher_name = Column(String)
    feed_publisher_url = Column(String)
    feed_lang = Column(String)
    feed_start_date = Column(Date)
    feed_end_date = Column(Date)
    feed_version = Column(String)
    feed_contact_email = Column(String)
    feed_contact_url = Column(String)

    # FeedInfo tablosunda primary key yok, bu durumda SQLAlchemy için bir ID ekleyelim
    id = Column(String, primary_key=True, default="default")

    __table_args__ = (
        UniqueConstraint('id', 'snapshot_id', name='uq_feed_info_snapshot'),
    )
