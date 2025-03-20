import logging
import traceback
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

from src.cat.common.config.BatchConfig import Batch
from src.cat.common.config.Config import Config
from src.cat.common.model.Response import error
from src.cat.hit.controllor import ok_controller

config = Config()
batch = Batch()
scheduler: BackgroundScheduler = batch.init_scheduler()


@asynccontextmanager
# 定义 lifespan 函数
async def lifespan(app: FastAPI):
    if scheduler is not None and not scheduler.running:
        logging.getLogger(__name__).info("Starting up...")
        scheduler.start()
    yield
    if scheduler is not None:
        logging.getLogger(__name__).info("Shutting down...")
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(ok_controller.router, prefix="/system")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    traceback.print_stack()
    return error(exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    traceback.print_stack()
    return error(exc)
