# uvicorn app:app --reload --host  192.168.78.49 --port 8000
import datetime
import json
import socket
import time
import datetime

from uvicorn import run
from fastapi.websockets import WebSocketState

from datetime import datetime, timedelta
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
# 统计集合数量以及名字
@app.websocket("/latest_location_data")
async def websocket_latest_location_data(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            # 初始化一个列表来存储每个集合的最新Loc_Address数据
            latest_location_data_list = []
            # 获取所有集合的名称
            collection_names = db.list_collection_names()
            # 遍历所有集合
            for collection_name in collection_names:
                collection = db[collection_name]
                # 查询每个集合中Loc_Address字段最新的数据
                # 假设每个文档都有一个名为"Timestamp"的时间戳字段
                latest_document = collection.find_one({}, sort=[('Timestamp', -1)])
                # 构建包含集合名称和最新Loc_Address数据的字典
                collection_data = {"collection_name": collection_name}
                if latest_document and "Loc_Address" in latest_document:
                    collection_data["latest_loc_address"] = latest_document["Loc_Address"]
                else:
                    collection_data["latest_loc_address"] = "No data or Loc_Address not found"
                # 将字典添加到列表中
                latest_location_data_list.append(collection_data)

            # 构建最终发送的数据结构，包含集合数量和集合数据列表
            final_data = {
                "total_collections": len(collection_names),
                "collections_data": latest_location_data_list
            }

            # 发送数据
            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(1)  # 暂停1秒，减少消息发送频率
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()



@app.websocket("/collection_stats")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection_stats = {}
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                # 统计不同分钟的数据量
                current_timestamp = int(time.time() * 1000)  # 当前时间戳转换为毫秒
                for i in range(10):  # 统计最近10分钟的数据量
                    start_timestamp = current_timestamp - (i + 1) * 60000  # 60000毫秒 * (i + 1)分钟
                    end_timestamp = current_timestamp - i * 60000  # 60000毫秒 * i分钟
                    count = collection.count_documents({
                        "Timestamp": {"$gte": start_timestamp, "$lt": end_timestamp}
                    })
                    # 将时间戳转换为datetime对象，然后格式化为小时:分钟格式
                    # 注意：datetime.fromtimestamp() 需要秒为单位，所以这里要将毫秒转换回秒
                    start_time_str = datetime.fromtimestamp(start_timestamp / 1000).strftime("%H:%M")
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
            # 初始化一个字典来存储每天的总数据量
            week_day_data_total = {}
            # 获取当前时间戳（毫秒）
            current_timestamp = int(time.time() * 1000)
            # 初始化每天的数据量为0
            for i in range(7):  # 从今天往前推7天
                start_timestamp = current_timestamp - (i + 1) * 86400000  # 一天的毫秒数
                start_date = time.strftime("%Y-%m-%d", time.localtime(start_timestamp / 1000))
                week_day_data_total[start_date] = 0  # 初始化每天的总数为0


            # 遍历所有集合
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                # 统计每天的数据量
                for i in range(7):  # 从今天往前推7天
                    start_timestamp = current_timestamp - (i + 1) * 86400000
                    end_of_day_timestamp = current_timestamp - i * 86400000
                    # 计算当前集合在当前天的数据量
                    count = collection.count_documents({
                        "Timestamp": {"$gte": start_timestamp, "$lt": end_of_day_timestamp}
                    })
                    # 更新总数据量
                    start_date = time.strftime("%Y-%m-%d", time.localtime(start_timestamp / 1000))
                    week_day_data_total[start_date] += count  # 累加每天的数据量

            # 发送每天的总数据量
            await websocket.send_text(json.dumps(week_day_data_total))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()


# 用于返回oreder页面的数据
@app.websocket("/latest_order_data")
async def websocket_latest_order_data(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            latest_order_data_list = []
            collection_names = db.list_collection_names()
            # 获取今天的日期范围
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = start_of_day + timedelta(days=1)
            # 转换为毫秒
            start_of_day_ms = int(start_of_day.timestamp() * 1000)
            end_of_day_ms = int(end_of_day.timestamp() * 1000)

            for collection_name in collection_names:
                collection = db[collection_name]
                daily_count = collection.count_documents({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    }
                })
                latest_document = collection.find_one({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    }
                }, sort=[('Timestamp', -1)])

                collection_data = {
                    "collection_name": collection_name,
                    "daily_count": daily_count
                }
                if latest_document:
                    # 将毫秒时间戳转换为正常的日期时间格式
                    latest_timestamp = datetime.fromtimestamp(latest_document.get("Timestamp", 0) / 1000)
                    collection_data.update({
                        "latest_loc_address": latest_document.get("Loc_Address", "No Loc_Address found"),
                        "latest_timestamp": latest_timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化日期时间
                        "latest_domain_type": latest_document.get("Domain_Type", "No Domain_Type found")
                    })
                else:
                    collection_data.update({
                        "latest_loc_address": "No data found",
                        "latest_timestamp": "No data found",
                        "latest_domain_type": "No data found"
                    })
                latest_order_data_list.append(collection_data)

            final_data = {
                "total_collections": len(collection_names),
                "collections_data": latest_order_data_list
            }

            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)  # 暂停1秒，减少消息发送频率
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

