from fastapi import APIRouter, HTTPException
from app.core.config import get_settings
import httpx

router = APIRouter()

@router.get("/mapbox/token_public", summary="Expose public Mapbox token")
def get_public_token():
    settings = get_settings()
    return {"token": settings.MAPBOX_PUBLIC_TOKEN}

@router.get("/mapbox/geocode", summary="Proxy to Mapbox Geocoding API")
async def geocode(q: str, limit: int = 5, language: str | None = None):
    settings = get_settings()
    if not settings.MAPBOX_SECRET_TOKEN:
        raise HTTPException(status_code=500, detail="MAPBOX_SECRET_TOKEN not set")

    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{q}.json"
    params = {
        "access_token": settings.MAPBOX_SECRET_TOKEN,
        "limit": limit,
    }
    if language:
        params["language"] = language

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
    if resp.status_code != 200:
        print(resp)
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
