import asyncio
import logging
import traceback

from fastapi import APIRouter
from fastapi.websockets import WebSocket

from src.cat.hit.model.Rank import Rank
from src.cat.hit.service.RankHolder import RankHolder

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 每秒调用一次 RankHolder().get_rank() 接口
            rank: [Rank] = RankHolder().get_rank()
            if rank is None or len(rank) == 0:
                # logging.getLogger(__name__).info("rank is None or len(rank) == 0")
                continue
            # 将 result_rising 转换为字典列表
            result_rising_dicts = [vars(rank) for rank in rank]
            # 发送 result_rising 数据
            await websocket.send_json(result_rising_dicts)
            # 等待 1 秒
            await asyncio.sleep(1)
    except Exception as e:
        logging.getLogger(__name__).info(f"Error sending data: {e}")
        traceback.print_exc()
    finally:
        if websocket.client_state.name == 'CONNECTED':
            await websocket.close()
