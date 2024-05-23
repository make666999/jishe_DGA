
import json
import socket
import time
import datetime
from uvicorn import run
from fastapi.websockets import WebSocketState
from datetime import datetime, timedelta
from fastapi import Request
from pymongo import MongoClient
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from bson.json_util import dumps
import asyncio
from starlette.responses import  FileResponse


app = FastAPI()

# 连接到MongoDB数据库
mongo_client = MongoClient("mongodb://886xt49626.goho.co:23904")
db = mongo_client["DGA"]
db2 = mongo_client["Data_pro"]


# 模板配置
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
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
            # 将结果转换为列表形式
            result = list(cursor)

            # 格式化数据
            formatted_data = {
                "total_collections": len(result),
                "collections_data": []
            }
            for item in result:
                collection_name = item["Device_Name"]
                latest_loc_address = item["last_loc_address"] if item["last_loc_address"] else "N/A"
                formatted_data["collections_data"].append({
                    "collection_name": collection_name,
                    "latest_loc_address": latest_loc_address
                })
            print(formatted_data)
            await websocket.send_text(json.dumps(formatted_data))
            await asyncio.sleep(1)  # 暂停10秒，减少消息发送频率

    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()
@app.websocket("/websocket_cluster_device_status")
async def websocket_websocket_cluster_device_status(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            # 初始化一个列表来存储每个集合的最新Loc_Address数据
            websocket_cluster_device_status_list = []
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
                websocket_cluster_device_status_list.append(collection_data)

            # 构建最终发送的数据结构，包含集合数量和集合数据列表
            final_data = {
                "total_collections": len(collection_names),
                "collections_data": websocket_cluster_device_status_list
            }

            # 发送数据
            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(1)  # 暂停10秒，减少消息发送频率
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()


# 处理集群统计数据的周期性轮询
@app.websocket("/websocket_poll_cluster_statistics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            websocket_poll_cluster_statistics = {}
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                # 统计不同分钟的数据量
                current_timestamp = int(time.time() * 1000)  # 当前时间戳转换为毫秒
                for i in range(10):  # 统计最近10分钟的数据量
                    start_timestamp = current_timestamp - (i + 1) * 60000
                    end_timestamp = current_timestamp - i * 60000
                    count = collection.count_documents({
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
            # 初始化一个字典来存储每天的总数据量
            websocket_weekly_data_total = {}
            current_timestamp = int(time.time() * 1000)
            for i in range(7):  # 从今天往前推7天
                start_timestamp = current_timestamp - (i + 1) * 86400000  # 一天的毫秒数
                start_date = time.strftime("%Y-%m-%d", time.localtime(start_timestamp / 1000))
                websocket_weekly_data_total[start_date] = 0  # 初始化每天的总数为0

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
                    websocket_weekly_data_total[start_date] += count  # 累加每天的数据量

            # 发送每天的总数据量
            await websocket.send_text(json.dumps(websocket_weekly_data_total))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()


# 管理集群设备列表和用户权限
@app.websocket("/websocket_user_list_management")
async def websocket_websocket_user_list_management(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            websocket_user_list_management_list = []
            collection_names = db.list_collection_names()
            # 获取今天的日期范围
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = start_of_day + timedelta(days=1)
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
                websocket_user_list_management_list.append(collection_data)

            final_data = {
                "total_collections": len(collection_names),
                "collections_data": websocket_user_list_management_list
            }

            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)  # 暂停5秒，减少消息发送频率
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()


#DNS流量数据安全状况统计分析
@app.websocket("/websocket_dns_traffic_security_analysis")
async def websocket_dns_traffic_security_analysis(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            stats_list = []
            collection_names = db.list_collection_names()
            # 获取今天的日期范围
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = start_of_day + timedelta(days=1)
            start_of_day_ms = int(start_of_day.timestamp() * 1000)
            end_of_day_ms = int(end_of_day.timestamp() * 1000)

            for collection_name in collection_names:
                collection = db[collection_name]
                # 统计Domain_Type为BENIGN的数量
                benign_count = collection.count_documents({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    },
                    "Domain_Type": "BENIGN"
                })
                # 统计Domain_Type不为BENIGN的数量
                non_benign_count = collection.count_documents({
                    "Timestamp": {
                        "$gte": start_of_day_ms,
                        "$lt": end_of_day_ms
                    },
                    "Domain_Type": {"$ne": "BENIGN"}
                })

                # 添加到统计列表
                stats_list.append({
                    "collection_name": collection_name,
                    "benign_count": benign_count,
                    "non_benign_count": non_benign_count
                })

            # 准备最终的数据
            final_data = {
                "total_collections": len(collection_names),
                "stats": stats_list
            }

            # 发送数据
            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)  # 暂停5秒，减少消息发送频率
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()


# 提供集群内域名访问的排名
@app.websocket("/websocket_daily_top_remain_type")
async def websocket_daily_top_remain_type(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            top_types_daily = []
            collection_names = db.list_collection_names()
            # 获取过去五天的日期
            now = datetime.now()
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
                    # 使用聚合管道查找每个集合在特定一天内Remain_Type出现的频率
                    pipeline = [
                        {"$match": {
                            "Timestamp": {"$gte": start_of_day_ms, "$lt": end_of_day_ms},
                            "Remote_Domain": {"$ne": None}  # 排除Remain_Type为null的文档
                        }},
                        {"$group": {
                            "_id": "$Remote_Domain",
                            "count": {"$sum": 1}
                        }},
                        {"$sort": {"count": -1}},
                        {"$limit": 1}
                    ]
                    results = list(collection.aggregate(pipeline))
                    for result in results:
                        remain_type = result['_id']
                        count = result['count']
                        if remain_type in total_counts:
                            total_counts[remain_type] += count
                        else:
                            total_counts[remain_type] = count

                # 找出出现频率最高的Remain_Type
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

            # 准备最终的数据
            final_data = {
                "top_types_daily": top_types_daily
            }

            # 发送数据
            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)  # 暂停5秒，减少消息发送频率
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()


async def get_latest_data():
    # 获取最新的十条数据
    latest_data = list(collection.find().sort("Timestamp", -1).limit(10))
    return latest_data

async def get_city_data():
    collection = db["GPU-SERVER"]
    query = {"moveLines": {"$ne": None}}
    projection = {"_id": 0,"moveLines": 1}
    city_data = collection.find(query,projection).sort("Timestamp", -1).limit(50)
    city_datas = [document["moveLines"] for document in city_data]
    city_data= {"moveLines":city_datas}
    return city_data



@app.websocket("/city_map")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            City_Data = await get_city_data()
            await websocket.send_text(dumps(City_Data))
            await asyncio.sleep(1)
    finally:
        # 关闭连接时的清理工作
        await websocket.close()




@app.post("/api/send_data")
async def receive_data(data: DataToReceive):
    # 在这里处理从前端发送过来的数据
    global db
    global collection
    collection= db[data.Local]
    print(data.Local)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"ipAddress":ipAddress})

@app.get("/index.html")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"ipAddress":ipAddress})

@app.get("/orders.html")
async def read_root(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request,"ipAddress":ipAddress})

@app.get("/order-detail.html")
async def read_root(request: Request):
    return templates.TemplateResponse("order-detail.html", {"request": request,"ipAddress":ipAddress})

@app.get("/customers.html")
async def read_root(request: Request):
    return templates.TemplateResponse("customers.html", {"request": request,"ipAddress":ipAddress})

@app.get("/mode-total.html")
async def read_root(request: Request):
    return templates.TemplateResponse("mode-total.html", {"request": request,"ipAddress":ipAddress})

@app.get("/Security_policy.html")
async def read_root(request: Request):
    return templates.TemplateResponse("Security_policy.html", {"request": request,"ipAddress":ipAddress})

@app.get("/flight.json")
async def read_root():
    import os

    current_path = os.getcwd()
    print("当前访问的路径是：", current_path)

    return FileResponse("templates/static/js/flight.json")

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

