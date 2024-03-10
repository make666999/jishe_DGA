# uvicorn app:app --reload --host  192.168.78.49 --port 8000
import datetime
import json
import socket
import time
import datetime

from uvicorn import run
from fastapi.websockets import WebSocketState
from datetime import timedelta

from fastapi import FastAPI, WebSocket, Request
from pymongo import MongoClient
import pymongo
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from bson.json_util import dumps
import asyncio

from starlette.responses import JSONResponse

app = FastAPI()

# 连接到MongoDB数据库
mongo_client = MongoClient("mongodb://8c630x9121.goho.co:23593")
db = mongo_client["DGA"]

# 模板配置
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

@app.websocket("/collection_stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection_stats = {}
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                # 统计不同分钟的数据量
                current_timestamp = int(time.time())
                for i in range(10):  # 统计最近10分钟的数据量
                    start_timestamp = current_timestamp - (i + 1) * 60  # 60秒 * (i + 1)分钟
                    end_timestamp = current_timestamp - i * 60  # 60秒 * i分钟
                    count = collection.count_documents({
                        "Timestamp": {"$gte": start_timestamp, "$lt": end_timestamp}
                    })
                    # 将时间戳转换为datetime对象，然后格式化为小时:分钟格式
                    start_time_str = datetime.datetime.fromtimestamp(start_timestamp).strftime("%H:%M")
                    collection_stats.setdefault(collection_name, {})[start_time_str] = count
            await websocket.send_text(json.dumps(collection_stats))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

class DataToReceive(BaseModel):
    Local: str
    Timestamp: int  # 接受整数类型的时间戳



# WebSocket 端点，用于返回数据库中所有表在每周每一天的数据总量
@app.websocket("/week_day_data_total")
async def websocket_week_day_data_total(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            week_day_data_total = {}
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                # 获取一周内每一天的起始时间戳和结束时间戳，并统计数据量
                current_timestamp = int(time.time())
                for i in range(7):  # 从今天往前推7天
                    start_timestamp = current_timestamp - (i + 1) * 86400  # 86400秒 = 一天的秒数
                    end_of_day_timestamp = current_timestamp - i * 86400
                    count = 0
                    data_points = collection.find({
                        "Timestamp": {"$gte": start_timestamp * 1000, "$lt": end_of_day_timestamp * 1000}
                    })
                    for data_point in data_points:
                        timestamp = data_point["Timestamp"] // 1000
                        six_second_interval = (timestamp - start_timestamp) // 5  # 计算六秒间隔
                        if six_second_interval in range(10):
                            count += 1
                    # 将时间戳转换为日期字符串，作为字典的键
                    start_date = time.strftime("%Y-%m-%d", time.localtime(start_timestamp))
                    week_day_data_total.setdefault(collection_name, {})[start_date] = count
            await websocket.send_text(json.dumps(week_day_data_total))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()




@app.post("/api/send_data")
async def receive_data(data: DataToReceive):
    # 在这里处理从前端发送过来的数据
    global db
    global collection
    collection= db[data.Local]
    print(data.Local)
    # received_data = data.dict()
    # return received_data


@app.get("/index.html")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"ipAddress":ipAddress})

def get_local_ip():
    try:
        # 创建一个socket连接
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个不存在的IP地址，以获取本地IP地址
        s.connect(("10.255.255.255", 1))
        # 获取本地IP地址
        local_ip = s.getsockname()[0]
        # 关闭连接
        s.close()
        return local_ip
    except Exception as e:
        print("Error occurred:", e)
        return None
ipAddress=str(get_local_ip())+":8000"

if __name__ == '__main__':
    local_ip = get_local_ip()
    run("app:app", host=f"{local_ip}", port=8000, reload=True)

