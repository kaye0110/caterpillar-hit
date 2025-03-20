import logging

from fastapi import APIRouter

from src.cat.common.model.Response import success

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ok")
async def ok():
    logging.getLogger(__name__).info("ok")
    return success(data="ok")
