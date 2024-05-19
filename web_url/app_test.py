import time
import datetime
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pymongo import MongoClient
from pyspark.sql.functions import col, from_unixtime, date_format
from fastapi.websockets import WebSocketState
import socket
from uvicorn import run
from fastapi import Request
from fastapi import FastAPI, WebSocket
import time
import json
import asyncio
from fastapi.websockets import WebSocket

app = FastAPI()

mongo_client = MongoClient("mongodb://886xt49626.goho.co:23904")
db = mongo_client["DGA"]


# 创建SparkSession，并指定MongoDB连接配置
my_spark = SparkSession \
    .builder \
    .appName("MongoDB Data Analysis") \
    .config("spark.mongodb.read.connection.uri", "mongodb://886xt49626.goho.co:23904") \
    .config("spark.mongodb.write.connection.uri", "mongodb://886xt49626.goho.co:23904") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.13:10.3.0") \
    .getOrCreate()
# # 读取MongoDB数据集合
# df = my_spark.read.format("mongodb").option("database", "DGA").option("collection", "GPU-SERVER").load()
#
# df.show()

def read_mongo(form_name):
    df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource") \
        .option("database", "DGA") \
        .option("collection", form_name) \
        .load()

    return df


def get_past_seven_days_data_count():
    collection_names = db.list_collection_names()

    # 获取当前时间戳
    current_timestamp = int(time.time())

    # 计算过去七天的时间戳范围
    start_timestamp = current_timestamp - 7 * 24 * 60 * 60
    end_timestamp = current_timestamp

    # 存储统计结果的字典，以日期为键，数据量为值
    statistics_dict = {}

    # 遍历过去七天的日期
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        statistics_dict[date] = 0

    # 遍历每个集合
    for form_name in collection_names:
        df = read_mongo(form_name)

        # 过滤出过去七天的数据
        df_filtered = df.filter((col("Timestamp") >= start_timestamp) & (col("Timestamp") < end_timestamp))

        # 将时间戳转换为日期
        df_filtered = df_filtered.withColumn("date", date_format(from_unixtime(col("Timestamp") / 1000), "yyyy-MM-dd"))

        # 统计每个日期的数据总量，并累加到统计结果字典中
        date_counts = df_filtered.groupBy("date").count().collect()
        for row in date_counts:
            date = row["date"]
            count = row["count"]
            statistics_dict[date] += count

    return statistics_dict

# 调用函数获取统计结果
statistics_result = get_past_seven_days_data_count()

# 打印统计结果
print(statistics_result)


# # 获取 MongoDB 中的所有集合名称
# collection_names = db.list_collection_names()
#
# # 遍历每个集合，获取过去七天的数据总量
# for collection_name in collection_names:
#     data_count = get_past_seven_days_data_count(collection_name)
#     print(f"Collection: {collection_name}, Past Seven Days Data Count: {data_count}")
# 将结果发送到WebSocket连接
# @app.websocket("/websocket_cluster_device_status")
# async def send_statistics_to_websocket(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while websocket.client_state == WebSocketState.CONNECTED:
#             # 查询数据库中所有集合名称
#             collection_names = db.list_collection_names()
#             for name in collection_names:
#                 print(name)
#             # 获取当前时间戳
#             current_timestamp = int(time.time())
#
#             # 计算过去七天的日期范围
#             start_timestamp = current_timestamp - 7 * 24 * 60 * 60
#             end_timestamp = current_timestamp
#
#             # 获取MongoDB中所有数据库的集合
#             collections = my_spark.read.format("mongo").option("uri",
#                                                             "mongodb://886xt49626.goho.co:23904/DGA").load().distinct()
#
#             # 遍历每个集合，统计过去七天的数据总量
#             statistics_dict = {}
#             for collection_row in collections.collect():
#                 collection_name = collection_row["name"]
#                 collection_df = my_spark.read.format("mongo").option("uri",
#                                                                   f"mongodb://886xt49626.goho.co:23904/{collection_name}").load()
#
#                 # 过滤出过去七天的数据
#                 df_filtered = collection_df.filter(
#                     (col("Timestamp") >= start_timestamp) & (col("Timestamp") < end_timestamp))
#
#                 # 将时间戳转换为日期，并按日期分组统计每天的数据总量
#                 df_stats = df_filtered.withColumn("date",
#                                                   date_format(from_unixtime(col("Timestamp") / 1000), "yyyy-MM-dd")) \
#                     .groupBy("date").count()
#
#                 # 将统计结果转换为字典格式
#                 daily_statistics = {row["date"]: row["count"] for row in df_stats.collect()}
#                 statistics_dict[collection_name] = daily_statistics
#
#             # 发送统计数据到WebSocket
#             await websocket.send_text(json.dumps(statistics_dict))
#             await asyncio.sleep(10)
#     except Exception as e:
#         print(f"错误: {e}")
#     finally:
#         await websocket.close()
#
#
#
# def get_local_ip():
#     try:
#         # 创建一个socket连接
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         # 连接到一个不存在的IP地址，以获取本地IP地址
#         s.connect(("10.255.255.255", 1))
#         # 获取本地IP地址
#         local_ip = s.getsockname()[0]
#         # 关闭连接
#         s.close()
#         return local_ip
#     except Exception as e:
#         print("Error occurred:", e)
#         return None
# ipAddress=str(get_local_ip())+":8000"
#
# if __name__ == '__main__':
#     local_ip = get_local_ip()
#     run("app_test:app", host=f"{local_ip}", port=8000, reload=True)