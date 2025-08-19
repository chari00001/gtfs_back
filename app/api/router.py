from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.mapbox import router as mapbox_router
from app.api.routes.gtfs import router as gtfs_router

# GTFS Tabloları için router'lar
from app.api.routes.agency import router as agency_router
from app.api.routes.routes import router as routes_router
from app.api.routes.stops import router as stops_router
from app.api.routes.trips import router as trips_router
from app.api.routes.stop_times import router as stop_times_router
from app.api.routes.calendar import router as calendar_router
from app.api.routes.calendar_dates import router as calendar_dates_router
from app.api.routes.shapes import router as shapes_router
from app.api.routes.fare_attributes import router as fare_attributes_router
from app.api.routes.fare_rules import router as fare_rules_router
from app.api.routes.feed_info import router as feed_info_router

api_router = APIRouter()

# Genel router'lar
api_router.include_router(health_router, tags=["health"], prefix="")
api_router.include_router(mapbox_router, tags=["mapbox"], prefix="")
api_router.include_router(gtfs_router, tags=["gtfs"], prefix="/gtfs")

# GTFS Tablo router'ları
api_router.include_router(agency_router, tags=["agency"], prefix="/agency")
api_router.include_router(routes_router, tags=["routes"], prefix="/routes")
api_router.include_router(stops_router, tags=["stops"], prefix="/stops")
api_router.include_router(trips_router, tags=["trips"], prefix="/trips")
api_router.include_router(stop_times_router, tags=["stop-times"], prefix="/stop-times")
api_router.include_router(calendar_router, tags=["calendar"], prefix="/calendar")
api_router.include_router(calendar_dates_router, tags=["calendar-dates"], prefix="/calendar-dates")
api_router.include_router(shapes_router, tags=["shapes"], prefix="/shapes")
api_router.include_router(fare_attributes_router, tags=["fare-attributes"], prefix="/fare-attributes")
api_router.include_router(fare_rules_router, tags=["fare-rules"], prefix="/fare-rules")
api_router.include_router(feed_info_router, tags=["feed-info"], prefix="/feed-info")

