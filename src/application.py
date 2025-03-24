import logging
import os
import traceback
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from src.cat.common.config.BatchConfig import Batch
from src.cat.common.config.Config import Config
from src.cat.common.model.Response import error
from src.cat.hit.controllor import ok_controller, futu_controller
from src.cat.hit.service.FutuService import FutuService




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

# 挂载静态文件目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
static_path = os.path.join(project_root, 'src', 'resource')
if os.path.exists(static_path) and os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    # 配置模板目录
    templates = Jinja2Templates(directory=static_path)
else:
    logging.getLogger(__name__).error(f"Static directory {static_path} does not exist.")

app.include_router(ok_controller.router, prefix="/system")
app.include_router(futu_controller.router, prefix="/futu")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    traceback.print_stack()
    return error(exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    traceback.print_stack()
    return error(exc)
