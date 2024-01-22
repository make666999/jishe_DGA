# main.py   uvicorn main:app --reload --host 192.168.78.71 --port 8000
from Tools.mongo_tools import mongo_link
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# 启用所有来源的跨源资源共享 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载前端静态文件
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# MongoDB 配置

db = mongo_link.mongo_link_database("DGA_IP_log")

# WebSocket 用于处理实时更新
class WebSocketManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_data(self, data: dict):
        for connection in self.connections:
            await connection.send_json(data)

websocket_manager = WebSocketManager()

@app.on_event("shutdown")
async def shutdown_event():
    db.close()

# API 端点用于获取最新数据
@app.get("/latest_data", response_class=HTMLResponse)
async def get_latest_data():
    return {"message": "访问 /ws 端点以获取实时更新."}

# MongoDB 查询以获取最新的10条记录
async def fetch_latest_data():
    collection = db["DGA_IP_now"]
    cursor = collection.find().sort("_id", -1).limit(10)
    return await cursor.to_list(length=10)

# WebSocket 端点用于发送实时数据
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await fetch_latest_data()
            await websocket_manager.send_data(data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
