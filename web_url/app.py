# # main.py
# import asyncio
#
# import mongo_link
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
#
# app = FastAPI()
#
# # 启用所有来源的跨源资源共享 (CORS)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # 挂载前端静态文件
# app.mount("/", StaticFiles(directory="D:/桌面/jishe_DGA/web_url/frontend", html=True), name="static")
#
# # MongoDB 配置
# db = mongo_link.mongo_link_database("DGA")
#
# # WebSocket 用于处理实时更新
# class WebSocketManager:
#     def __init__(self):
#         self.connections = []
#         self.lock = asyncio.Lock()
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.connections.remove(websocket)
#
#     async def send_data(self, data: dict):
#         async with self.lock:
#             for connection in self.connections:
#                 await connection.send_json(data)
#
# websocket_manager = WebSocketManager()
#
# # MongoDB 连接关闭
# @app.on_event("shutdown")
# async def shutdown_event():
#     db.close()
#
# # API 端点用于获取最新数据
# @app.get("/latest_data")
#
# async def get_latest_data():
#     latest_data = await fetch_latest_data()
#     return {"latest_data": latest_data}
#
# # MongoDB 查询以获取最新的10条记录
# async def fetch_latest_data():
#     collection = db["DGA"]
#     cursor = collection.find().sort("timestamp", -1).limit(10)
#
# # 将游标转换为列表
#     latest_records = list(cursor)
#
# # 打印查询结果
#     for record in latest_records:
#         print(record)
#     return await cursor.to_list(length=10)
#
# # WebSocket 端点用于发送实时数据
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket_manager.connect(websocket)
#     try:
#         while True:
#             data = await fetch_latest_data()
#             await websocket_manager.send_data(data)
#             await asyncio.sleep(1)
#     except WebSocketDisconnect:
#         websocket_manager.disconnect(websocket)
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
db = mongo_client["WEB_TEST"]
collection = db["DGA_IP_now"]
# 模板配置
templates = Jinja2Templates(directory="templates")


async def get_latest_data():
    # 获取最新的十条数据
    latest_data = list(collection.find().sort("timestamp", -1).limit(10))
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


