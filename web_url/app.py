import json
import socket

from pymongo import DESCENDING
from starlette.websockets import WebSocketDisconnect

import time
import datetime
from uvicorn import run
from fastapi.websockets import WebSocketState
from datetime import datetime, timedelta
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from bson.json_util import dumps
import asyncio
from starlette.responses import FileResponse

app = FastAPI()

# 连接到MongoDB数据库
mongo_client = AsyncIOMotorClient("mongodb://886xt49626.goho.co:23904")
db = mongo_client["DGA"]
db2 = mongo_client["Data_pro"]

# 模板配置
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

day_counts = 0

# 统计集合数量以及名字
@app.websocket("/websocket_get_data_formatted")
async def get_data_formatted(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection = db2["test"]
            # 使用聚合管道查询Device_Name列和last_loc_address
            pipeline = [
                {"$project": {"Device_Name": 1, "last_loc_address": 1, "_id": 0}}
            ]
            cursor = collection.aggregate(pipeline)
            result = await cursor.to_list(length=None)  # 异步转换为列表

            # 格式化数据
            formatted_data = {
                "total_collections": len(result),
                "collections_data": [],
                "on_online": 0
            }
            on_online = 0
            for item in result:
                collection_name = item["Device_Name"]
                latest_loc_address = item["last_loc_address"] if item["last_loc_address"] else "未上线"
                if latest_loc_address != "未上线":
                    on_online += 1
                formatted_data["collections_data"].append({
                    "collection_name": collection_name,
                    "latest_loc_address": latest_loc_address,
                })
            formatted_data["on_online"] = on_online

            await websocket.send_text(json.dumps(formatted_data))
            await asyncio.sleep(10)  # 暂停10秒，减少消息发送频率

    except Exception as e:
        print(f"错误统计集合数量以及名字: {e}")
    finally:
        await websocket.close()

# 处理集群统计数据的周期性轮询
@app.websocket("/websocket_poll_cluster_statistics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            websocket_poll_cluster_statistics = {}
            for collection_name in await db.list_collection_names():
                collection = db[collection_name]
                current_timestamp = int(time.time() * 1000)  # 当前时间戳转换为毫秒
                for i in range(10):  # 统计最近10分钟的数据量
                    start_timestamp = current_timestamp - (i + 1) * 60000
                    end_timestamp = current_timestamp - i * 60000
                    count = await collection.count_documents({
                        "Timestamp": {"$gte": start_timestamp, "$lt": end_timestamp}
                    })

                    # 注意：datetime.fromtimestamp() 需要秒为单位，所以这里要将毫秒转换回秒
                    start_time_str = datetime.fromtimestamp(start_timestamp / 1000).strftime("%H:%M")
                    websocket_poll_cluster_statistics.setdefault(collection_name, {})[start_time_str] = count
            await websocket.send_text(json.dumps(websocket_poll_cluster_statistics))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

class DataToReceive(BaseModel):
    Local: str
    Timestamp: int

# 提供集群内DNS流量的周报告
@app.websocket("/websocket_weekly_data_total")
async def websocket_websocket_weekly_data_total(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            websocket_weekly_data_total = {}
            current_timestamp = int(time.time() * 1000)
            for i in range(7):  # 从今天往前推7天
                start_timestamp = current_timestamp - (i + 1) * 86400000  # 一天的毫秒数
                start_date = time.strftime("%Y-%m-%d", time.localtime(start_timestamp / 1000))
                websocket_weekly_data_total[start_date] = 0  # 初始化每天的总数为0

            for collection_name in await db.list_collection_names():
                collection = db[collection_name]
                for i in range(7):  # 从今天往前推7天
                    start_timestamp = current_timestamp - (i + 1) * 86400000
                    end_of_day_timestamp = current_timestamp - i * 86400000
                    count = await collection.count_documents({
                        "Timestamp": {"$gte": start_timestamp, "$lt": end_of_day_timestamp}
                    })
                    start_date = time.strftime("%Y-%m-%d", time.localtime(start_timestamp / 1000))
                    websocket_weekly_data_total[start_date] += count  # 累加每天的数据量

            await websocket.send_text(json.dumps(websocket_weekly_data_total))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"错误提供集群内DNS流量的周报告: {e}")
    finally:
        await websocket.close()

# 管理集群设备列表和用户权限
@app.websocket("/websocket_user_list_management")
async def websocket_websocket_user_list_management(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            websocket_user_list_management_list = []
            collection_names = await db.list_collection_names()
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = start_of_day + timedelta(days=1)
            start_of_day_ms = int(start_of_day.timestamp() * 1000)
            end_of_day_ms = int(end_of_day.timestamp() * 1000)

            for collection_name in collection_names:
                collection = db[collection_name]
                daily_count = await collection.count_documents({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    }
                })
                latest_document = await collection.find_one({
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
                    latest_timestamp = datetime.fromtimestamp(latest_document.get("Timestamp", 0) / 1000)
                    collection_data.update({
                        "latest_loc_address": latest_document.get("Loc_Address", "No Loc_Address found"),
                        "latest_timestamp": latest_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        "latest_domain_type": latest_document.get("Domain_Type", "No Domain_Type found")
                    })
                else:
                    collection_data.update({
                        "latest_loc_address": "No data found",
                        "latest_timestamp": "No data found",
                        "latest_domain_type": "No data found"
                    })
                websocket_user_list_management_list.append(collection_data)

            final_data = {
                "total_collections": len(collection_names),
                "collections_data": websocket_user_list_management_list
            }

            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)
    except Exception as e:
        print(f"错误管理集群设备列表和用户权限: {e}")
    finally:
        await websocket.close()

# DNS流量数据安全状况统计分析
@app.websocket("/websocket_dns_traffic_security_analysis")
async def websocket_dns_traffic_security_analysis(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            stats_list = []
            global day_counts
            collection_names = await db.list_collection_names()
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = start_of_day + timedelta(days=1)
            start_of_day_ms = int(start_of_day.timestamp() * 1000)
            end_of_day_ms = int(end_of_day.timestamp() * 1000)

            for collection_name in collection_names:
                collection = db[collection_name]
                benign_count = await collection.count_documents({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    },
                    "Domain_Type": "BENIGN"
                })
                non_benign_count = await collection.count_documents({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    },
                    "Domain_Type": {"$ne": "BENIGN"}
                })
                stats_list.append({
                    "collection_name": collection_name,
                    "benign_count": benign_count,
                    "non_benign_count": non_benign_count
                })

            day_counts = stats_list[0]["benign_count"] + stats_list[0]["non_benign_count"]
            final_data = {
                "total_collections": len(collection_names),
                "stats": stats_list,
                "day_counts": day_counts
            }

            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)
    except Exception as e:
        print(f"错误DNS流量数据安全状况统计分析: {e}")
    finally:
        await websocket.close()

# 提供集群内域名访问的排名--实时
@app.websocket("/websocket_daily_top_remain_type")
async def websocket_daily_top_remain_type(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            top_types_daily = []
            collection_names = await db.list_collection_names()
            now = datetime.now()
            today_count = 0

            for day_back in range(5):
                specific_day = now - timedelta(days=day_back)
                start_of_day = datetime(specific_day.year, specific_day.month, specific_day.day)
                end_of_day = start_of_day + timedelta(days=1)
                start_of_day_ms = int(start_of_day.timestamp() * 1000)
                end_of_day_ms = int(end_of_day.timestamp() * 1000)

                daily_top_type = {}
                total_counts = {}

                for collection_name in collection_names:
                    collection = db[collection_name]
                    pipeline = [
                        {"$match": {
                            "Timestamp": {"$gte": start_of_day_ms, "$lt": end_of_day_ms},
                            "Remote_Domain": {"$ne": None}
                        }},
                        {"$group": {
                            "_id": "$Remote_Domain",
                            "count": {"$sum": 1}
                        }},
                        {"$sort": {"count": -1}},
                        {"$limit": 1}
                    ]
                    results = await collection.aggregate(pipeline).to_list(length=None)
                    for result in results:
                        remain_type = result['_id']
                        count = result['count']
                        if remain_type in total_counts:
                            total_counts[remain_type] += count
                        else:
                            total_counts[remain_type] = count
                        if day_back == 0:
                            today_count += count

                if total_counts:
                    top_remain_type = max(total_counts, key=total_counts.get)
                    daily_top_type['date'] = start_of_day.strftime('%m-%d')
                    daily_top_type['top_remain_type'] = top_remain_type
                    daily_top_type['count'] = total_counts[top_remain_type]
                else:
                    daily_top_type['date'] = start_of_day.strftime('%m-%d')
                    daily_top_type['top_remain_type'] = 'None'
                    daily_top_type['count'] = 0

                top_types_daily.append(daily_top_type)

            final_data = {
                "top_types_daily": top_types_daily,
                "today_total_count": today_count
            }

            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)
    except Exception as e:
        print(f"错误访问的排名: {e}")
    finally:
        await websocket.close()

# customer.html.流量消息发送
@app.websocket("/websocket_last_messages")
async def websocket_last_messages(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection_names = sorted(await db.list_collection_names())
            websocket_user_list_management_list = []

            for collection_name in collection_names:
                collection = db[collection_name]
                recent_documents = collection.find(
                    {},
                    projection={"Domain_Address": 1, "Remote_Domain": 1, "toName": 1, "Domain_Type": 1, "Timestamp": 1},
                    sort=[('Timestamp', DESCENDING)],
                    limit=27
                )

                recent_data = []
                count = 0

                async for doc in recent_documents:
                    try:
                        timestamp_int = int(doc['Timestamp'])
                        timestamp = datetime.fromtimestamp(timestamp_int / 1000)
                        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        formatted_timestamp = "Invalid timestamp"
                        continue

                    doc_data = {
                        "collection_name": collection_name,
                        "Domain_Address": doc.get("Domain_Address", "No data found"),
                        "Remote_Domain": doc.get("Remote_Domain", "No data found"),
                        "toName": doc.get("toName", "No data found"),
                        "Domain_Type": doc.get("Domain_Type", "No data found"),
                        "Timestamp": formatted_timestamp
                    }
                    recent_data.append(doc_data)
                    count += 1
                    if count >= 30:
                        break

                websocket_user_list_management_list.extend(recent_data)

            await websocket.send_json(websocket_user_list_management_list)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error in managing cluster device list and user permissions: {e}")
    finally:
        await websocket.close()

# customer.html.  total_nineth_counts
@app.websocket("/total_nineth_counts")
async def total_nineth_counts(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection = db2["test"]
            recent_documents = collection.find(
                {},
                projection={"Week_Statistics": 1},
                limit=9
            )

            data = {
                "time": [],
                "data_counts": []
            }

            async for doc in recent_documents:
                week_statistics = doc.get("Week_Statistics", {})
                sorted_dates = sorted(week_statistics.keys(), reverse=True)[:9]
                for date in sorted_dates:
                    count = week_statistics[date]
                    if date not in data["time"]:
                        data["time"].append(date)
                        data["data_counts"].append(count)
                    else:
                        index = data["time"].index(date)
                        data["data_counts"][index] += count

            combined = sorted(zip(data["time"], data["data_counts"]), key=lambda x: x[0])
            data["time"], data["data_counts"] = zip(*combined) if combined else ([], [])

            await websocket.send_json(data)
            await asyncio.sleep(600)
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error in managing cluster device list and user permissions: {e}")
    finally:
        await websocket.close()

async def get_city_data():
    collection = db["GPU-SERVER"]
    pipeline = [
        {"$match": {"moveLines": {"$ne": None}, "moveLines.coords": {"$exists": True}}},
        {"$project": {"coords": "$moveLines.coords", "_id": 0}},
        {"$group": {"_id": "$coords"}},
        {"$limit": 5000}
    ]
    print("这是异步app")
    city_data = collection.aggregate(pipeline)
    unique_coords = set()

    async for document in city_data:
        coords = tuple(map(tuple, document["_id"]))
        unique_coords.add(coords)

    all_coords = list(unique_coords)
    return all_coords

@app.websocket("/city_map")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            City_Data = await get_city_data()
            await websocket.send_text(dumps(City_Data))
            await asyncio.sleep(60)
    finally:
        await websocket.close()

class DataToReceive(BaseModel):
    code_types: str
    new_model_value: str

@app.post("/api/send_data")
async def receive_data(data: DataToReceive):
    print("Received data:", data)
    collection = db2["test"]
    first_doc = await collection.find_one({}, projection={'model': 1})
    print('原始数据：', first_doc)
    original_model = 0
    safer_model = ['安全等级', '漏洞预警', '风险巡航', '策略偏向']
    if first_doc and 'model' in first_doc:
        original_model = first_doc['model']
    if data.code_types == 'model_code':
        modified_model = data.new_model_value + original_model[2:]
        update_result = await collection.update_many(
            {},
            {'$set': {'model': modified_model}}
        )
        print('修改之后：', modified_model)
        if update_result.modified_count > 0:
            return {"message": "Updated model successfully."}
        else:
            return {"message": "No documents were updated."}
    elif data.code_types == '安全等级' or data.code_types == '漏洞预警' or data.code_types == '风险巡航' or data.code_types == '策略偏向':
        safer_model_index = safer_model.index(data.code_types)
        modified_model = original_model[:2 + safer_model_index] + data.new_model_value + original_model[3 + safer_model_index:]
        update_result = await collection.update_many(
            {},
            {'$set': {'model': modified_model}}
        )
        print('修改之后：', modified_model)
        if update_result.modified_count > 0:
            return {"message": "Updated model successfully."}
        else:
            return {"message": "No documents were updated."}
    else:
        print('no model_code')
        return {"message": "Code type is not model_code."}

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "ipAddress": ipAddress})

@app.get("/index.html")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "ipAddress": ipAddress})

@app.get("/orders.html")
async def read_root(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request, "ipAddress": ipAddress})

@app.get("/order-detail.html")
async def read_root(request: Request):
    return templates.TemplateResponse("order-detail.html", {"request": request, "ipAddress": ipAddress})

@app.get("/customers.html")
async def read_root(request: Request):
    return templates.TemplateResponse("customers.html", {"request": request, "ipAddress": ipAddress})

@app.get("/mode-total.html")
async def read_root(request: Request):
    return templates.TemplateResponse("mode-total.html", {"request": request, "ipAddress": ipAddress})

@app.get("/Security_policy.html")
async def read_root(request: Request):
    return templates.TemplateResponse("Security_policy.html", {"request": request, "ipAddress": ipAddress})

@app.get("/flight.json")
async def read_root():
    import os

    current_path = os.getcwd()
    print("当前访问的路径是：", current_path)

    return FileResponse("templates/static/js/flight.json")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Error occurred:", e)
        return None

ipAddress = str(get_local_ip()) + ":8000"

if __name__ == '__main__':
    local_ip = get_local_ip()
    run("app:app", host=f"{local_ip}", port=8000, reload=True)
