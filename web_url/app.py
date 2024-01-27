# uvicorn app:app --reload --host 192.168.78.49 --port 8000
# 192.168.78.49
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

@app.get("/type")
async def read_root(request: Request):
    return templates.TemplateResponse("type.html", {"request": request})
