from fastapi import APIRouter

from src.entrypoints.http.api.v1.endpoints.item import item_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(item_router)
