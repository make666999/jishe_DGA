
import json
import socket

from starlette.websockets import WebSocketDisconnect

import time
import datetime
from uvicorn import run
from fastapi.websockets import WebSocketState
from datetime import datetime, timedelta
from fastapi import Request
from pymongo import MongoClient, DESCENDING
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from bson.json_util import dumps
import asyncio
from starlette.responses import  FileResponse


app = FastAPI()

# 连接到MongoDB数据库
# mongo_client = MongoClient("mongodb://886xt49626.goho.co:23904")
mongo_client = MongoClient("mongodb://886xt49626.goho.co:23904")
db = mongo_client["DGA"]
db2 = mongo_client["Data_pro"]


# 模板配置
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

day_counts=0
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
                "collections_data": [],
                "on_online": 0
            }
            on_online=0
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
            print(formatted_data)
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
        print(f"错误管理集群设备列表和用户权限: {e}")
    finally:
        await websocket.close()


#DNS流量数据安全状况统计分析
@app.websocket("/websocket_dns_traffic_security_analysis")
async def websocket_dns_traffic_security_analysis(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            stats_list = []
            global day_counts  # 声明你要使用全局变量
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

            day_counts = stats_list[0]["benign_count"] + stats_list[0]["non_benign_count"]
            # 准备最终的数据
            final_data = {
                "total_collections": len(collection_names),
                "stats": stats_list,
                "day_counts": day_counts
            }



            # 发送数据
            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)  # 暂停5秒，减少消息发送频率
    except Exception as e:
        print(f"错误DNS流量数据安全状况统计分析: {e}")
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
            now = datetime.now()
            today_count = 0  # 初始化今日域名总量计数器

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
                    # 使用聚合管道查找每个集合在特定一天内Remote_Domain出现的频率
                    pipeline = [
                        {"$match": {
                            "Timestamp": {"$gte": start_of_day_ms, "$lt": end_of_day_ms},
                            "Remote_Domain": {"$ne": None}  # 排除Remote_Domain为null的文档
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
                        if day_back == 0:  # 仅对今日数据进行总计
                            today_count += count

                # 找出出现频率最高的Remote_Domain
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
                "top_types_daily": top_types_daily,
                "today_total_count": today_count  # 添加今日域名总量
            }

            # 发送数据
            await websocket.send_text(json.dumps(final_data))
            await asyncio.sleep(5)  # 暂停5秒，减少消息发送频率
    except Exception as e:
        print(f"错误访问的排名: {e}")
    finally:
        await websocket.close()

#customer.html.流量消息发送
@app.websocket("/websocket_last_messages")
async def websocket_last_messages(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection_names = sorted(db.list_collection_names())  # 排序集合名称

            websocket_user_list_management_list = []

            for collection_name in collection_names:
                collection = db[collection_name]
                # 按时间戳降序排序并限制数量为10
                recent_documents = collection.find(
                    {},
                    projection={"Domain_Address": 1, "Remote_Domain": 1, "toName": 1, "Domain_Type": 1, "Timestamp": 1},
                    sort=[('Timestamp', DESCENDING)],
                    limit=27
                )

                recent_data = []
                count = 0  # 设置计数器

                for doc in recent_documents:
                    try:
                        timestamp_int = int(doc['Timestamp'])
                        timestamp = datetime.fromtimestamp(timestamp_int / 1000)
                        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        formatted_timestamp = "Invalid timestamp"
                        continue  # 如果时间戳无效，跳过当前文档

                    doc_data = {
                        "collection_name": collection_name,
                        "Domain_Address": doc.get("Domain_Address", "No data found"),
                        "Remote_Domain": doc.get("Remote_Domain", "No data found"),
                        "toName": doc.get("toName", "No data found"),
                        "Domain_Type": doc.get("Domain_Type", "No data found"),
                        "Timestamp": formatted_timestamp
                    }
                    recent_data.append(doc_data)
                    count += 1  # 每处理一条数据，计数器加一
                    if count >= 30:
                        break  # 当计数器达到10时，停止处理该集合的数据

                websocket_user_list_management_list.extend(recent_data)

            # 将数据以 JSON 格式发送给客户端
            await websocket.send_json(websocket_user_list_management_list)
            await asyncio.sleep(1)  # 暂停5秒，减少消息发送频率
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error in managing cluster device list and user permissions: {e}")
    finally:
        await websocket.close()
#customer.html.  total_nineth_counts
@app.websocket("/total_nineth_counts")
async def total_nineth_counts(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            collection = db2["test"]
            recent_documents = collection.find(
                {},
                projection={"Week_Statistics": 1},
                limit=9  # 保证我们最多处理9个文档
            )

            # 初始化数据结构
            data = {
                "time": [],
                "data_counts": []
            }

            # 遍历文档
            for doc in recent_documents:
                week_statistics = doc.get("Week_Statistics", {})
                # 从所有统计数据中提取最新的九个日期
                sorted_dates = sorted(week_statistics.keys(), reverse=True)[:9]
                for date in sorted_dates:
                    count = week_statistics[date]
                    if date not in data["time"]:
                        data["time"].append(date)
                        data["data_counts"].append(count)
                    else:
                        index = data["time"].index(date)
                        data["data_counts"][index] += count

            # 按日期顺序重新排序数据
            combined = sorted(zip(data["time"], data["data_counts"]), key=lambda x: x[0])
            data["time"], data["data_counts"] = zip(*combined) if combined else ([], [])

            # 将数据以 JSON 格式发送给客户端
            await websocket.send_json(data)
            await asyncio.sleep(600)  # 暂停10分钟，减少消息发送频率
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error in managing cluster device list and user permissions: {e}")
    finally:
        await websocket.close()


async def get_city_data():
    collection = db["GPU-SERVER"]
    # 使用聚合框架进行查询和去重
    pipeline = [
        {"$match": {"moveLines": {"$ne": None}, "moveLines.coords": {"$exists": True}}},  # 筛选包含 coords 的文档
        {"$project": {"coords": "$moveLines.coords", "_id": 0}},  # 投影 coords 字段
        {"$group": {"_id": "$coords"}},  # 按 coords 字段进行分组，实现去重
        {"$limit": 5000}  # 限制最多返回 50000 个结果
    ]
    city_data = collection.aggregate(pipeline)

    # 创建一个列表来存储每个唯一的 coords
    unique_coords = set()

    # 遍历聚合结果
    for document in city_data:
        coords = tuple(map(tuple, document["_id"]))  # 转换列表的列表为元组的元组
        unique_coords.add(coords)

    # 将集合转换回列表
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
        # 关闭连接时的清理工作
        await websocket.close()


class DataToReceive(BaseModel):
    code_types: str
    new_model_value: str



@app.post("/api/send_data")
async def receive_data(data: DataToReceive):
    print("Received data:", data)
    collection = db2["test"]
    first_doc = collection.find_one({}, projection={'model': 1})
    print('原始数据：',first_doc)
    original_model = 0
    safer_model=['安全等级','漏洞预警','风险巡航','策略偏向']
    if first_doc and 'model' in first_doc:
        original_model = first_doc['model']
    if data.code_types == 'model_code':
            # 修改model值的前两位
            modified_model = data.new_model_value + original_model[2:]
            update_result = collection.update_many(
                {},
                {'$set': {'model': modified_model}}
            )
            print('修改之后：', modified_model)
            if update_result.modified_count > 0:
                return {"message": "Updated model successfully."}
            else:
                return {"message": "No documents were updated."}
    elif data.code_types == '安全等级' or data.code_types == '漏洞预警' or data.code_types == '风险巡航' or data.code_types == '策略偏向':
        safer_model_index=safer_model.index(data.code_types)
        modified_model = original_model[:2+safer_model_index]+data.new_model_value + original_model[3+safer_model_index:]
        update_result = collection.update_many(
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

