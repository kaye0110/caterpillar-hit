import os
from typing import Any, Optional

from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.responses import StreamingResponse


class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[Any] = {}


def create_response(status: str, message: str, data: Any = None):
    response = ResponseModel(status=status, message=message, data=data)
    return JSONResponse(content=response.dict())


def error(e: Exception, data: Any = None):
    return fault(message=str(e), data=data)


def fault(status: str = 500, message: str = 'Unknown Exception', data: Any = None):
    return create_response(status=status, message=message, data=data)


def success(data: Any = None):
    return create_response(status='200', message='Success', data=data)


def download_file(file_path: str):
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        return Response("File not found", status_code=404)

    # 读取文件并返回
    file_like = open(file_path, mode="rb")

    return StreamingResponse(file_like, media_type="application/octet-stream", headers={
        "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
    })
