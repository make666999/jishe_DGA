# uvicorn app:app --reload --host 192.168.78.71 --port 8000
import datetime
import json
import time

from fastapi.websockets import WebSocketState

from fastapi import FastAPI, WebSocket, Request
from pymongo import MongoClient
import pymongo
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bson.json_util import dumps
import asyncio

from starlette.responses import JSONResponse

app = FastAPI()

# 连接到MongoDB数据库
mongo_client = MongoClient("mongodb://8c630x9121.goho.co:23593")
db = mongo_client["DGA"]
collection = db["GPU-SERVER"]
# 模板配置
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")



# 获取列表分类

today = datetime.date.today().strftime("%Y-%m-%d")

async def get_data_list():
    # 获取当天的起始时间戳和结束时间戳
    start_of_day = int(time.mktime(datetime.datetime.strptime(today, "%Y-%m-%d").timetuple()) * 1000)
    end_of_day = start_of_day + 86400000  # 一天的毫秒数

    # 使用聚合框架执行统计操作
    pipeline = [
        {"$match": {"Domain_Type": "BENIGN", "Timestamp": {"$gte": start_of_day, "$lt": end_of_day}}},
        {"$group": {"_id": None, "Good": {"$sum": 1}}}
    ]
    response_count = list(collection.aggregate(pipeline))

    # 获取非"BENIGN"类型的数据数量
    non_response_count = collection.count_documents({"Domain_Type": {"$ne": "BENIGN"}, "Timestamp": {"$gte": start_of_day, "$lt": end_of_day}})
    return {
        "Good": response_count[0]["Good"] if response_count else 0,
        "Bad": non_response_count
    }

@app.websocket("/data_list")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            data_list = await get_data_list()
            print("data_list:", data_list)
            await websocket.send_text(dumps(data_list))
            await asyncio.sleep(1)
    except Exception as e:
            print(f"Error: {e}")
    finally:
        # 关闭连接时的清理工作
        await websocket.close()

# 统计不同时间的数据
async def get_data_count_per_second():
    # 获取当前时间并只计算一次
    current_timestamp = int(time.time() * 1000)
    ten_seconds_ago = current_timestamp - 10000

    data_points = collection.find({
        "Timestamp": {"$gte": ten_seconds_ago, "$lte": current_timestamp}
    })
    results = list(data_points)
    return results

@app.websocket("/data_per_second")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            data_per_second = await get_data_count_per_second()
            print("data_per_second:", data_per_second)
            await websocket.send_text(dumps(data_per_second))
            await asyncio.sleep(1)
    except Exception as e:
            print(f"Error: {e}")
    finally:
        # 关闭连接时的清理工作
        await websocket.close()


# 统计当前前60秒每隔5秒内的数据数量
async def get_count_per_six_seconds():
    current_timestamp = int(time.time() * 1000)
    sixty_seconds_ago = current_timestamp - 60000

    data_points = collection.find({
        "Timestamp": {"$gte": sixty_seconds_ago, "$lte": current_timestamp}
    })

    # 初始化每个六秒间隔的数据计数为0
    data_per_six_seconds = {i: 0 for i in range(10)}

    for data_point in data_points:
        timestamp = data_point["Timestamp"]
        six_second_interval = (timestamp - sixty_seconds_ago) // 6000  # 计算六秒间隔
        if six_second_interval in data_per_six_seconds:
            data_per_six_seconds[six_second_interval] += 1

    # 准备返回的数据
    times = []
    counts = []
    for i in range(10):
        time_str = time.strftime("%H:%M:%S", time.localtime((sixty_seconds_ago // 1000) + (i * 6)))
        times.append(time_str)
        counts.append(data_per_six_seconds[i])

    return {"data": times, "count": counts}

@app.websocket("/count_per_six_seconds")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            result = await get_count_per_six_seconds()
            await websocket.send_text(json.dumps(result))  # 使用json.dumps将字典转换为JSON字符串
            await asyncio.sleep(6)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()





# 获取十条最新数据和地图数据
async def get_latest_data():
    # 获取最新的十条数据
    latest_data = list(collection.find().sort("Timestamp", -1).limit(10))
    return latest_data

async def get_city_data():
    query = {"moveLines": {"$ne": None}}
    projection = {"_id": 0,"moveLines": 1}

    city_data = collection.find(query,projection).sort("Timestamp", -1).limit(50)
    city_datas = [document["moveLines"] for document in city_data]
    city_data= {"moveLines":city_datas}
    # city_data = {"moveLines": document["moveLines"] for document in city_data}
    return city_data





@app.websocket("/city_map")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            City_Data = await get_city_data()
            print("City Data:", City_Data)
            await websocket.send_text(dumps(City_Data))
            await asyncio.sleep(1)
    finally:
        # 关闭连接时的清理工作
        await websocket.close()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            latest_data = await get_latest_data()
            print("Latest Data:", latest_data)
            await websocket.send_text(dumps(latest_data))
            await asyncio.sleep(1)
    except:
        print("Error")
    finally:
        # 关闭连接时的清理工作
        await websocket.close()


@app.get("/")
async def read_root(request: Request):
    latest_data = await get_latest_data()
    return templates.TemplateResponse("index.html", {"request": request, "latest_data": latest_data})


@app.get("/data_ui")
async def read_root(request: Request):
    city_data = await get_city_data()
    print(city_data)
    return templates.TemplateResponse("data_ui.html", {"request": request, "allDataParam": city_data})

@app.get("/index")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/id")
async def read_root(request: Request):
    return templates.TemplateResponse("database.html", {"request": request})

@app.get("/database")
async def read_root(request: Request):
    return templates.TemplateResponse("database.html", {"request": request})

@app.get("/type")
async def read_root(request: Request):
    return templates.TemplateResponse("type.html", {"request": request})