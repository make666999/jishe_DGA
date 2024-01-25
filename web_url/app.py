# uvicorn app:app --reload --host 192.168.78.71 --port 8000

from fastapi.websockets import WebSocketState

from fastapi import FastAPI, WebSocket, Request
from pymongo import MongoClient

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bson.json_util import dumps
import asyncio

app = FastAPI()

# 连接到MongoDB数据库


mongo_client = MongoClient("mongodb://8c630x9121.goho.co:23593")
db = mongo_client["DGA"]
collection = db["DGA_Domain_Log"]
# 模板配置
templates = Jinja2Templates(directory="templates")


async def get_latest_data():
    # 获取最新的十条数据
    latest_data = list(collection.find().sort("Timestamp", -1).limit(10))
    return latest_data




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            latest_data = await get_latest_data()
            print("Latest Data:", latest_data)
            await websocket.send_text(dumps(latest_data))
            await asyncio.sleep(1)
    finally:
        # 关闭连接时的清理工作
        await websocket.close()


@app.get("/")
async def read_root(request: Request):
    latest_data = await get_latest_data()
    return templates.TemplateResponse("index.html", {"request": request, "latest_data": latest_data})

