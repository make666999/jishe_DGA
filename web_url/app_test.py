from pyspark.sql import SparkSession
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

# 创建SparkSession，并指定MongoDB连接配置
my_spark = SparkSession \
    .builder \
    .appName("MongoDB Data Analysis") \
    .config("spark.mongodb.read.connection.uri", "mongodb://886xt49626.goho.co:23904/DGA.GPU-SERVER") \
    .config("spark.mongodb.write.connection.uri", "mongodb://886xt49626.goho.co:23904/DGA.GPU-SERVER") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.13:10.3.0") \
    .getOrCreate()

# # 读取MongoDB数据集合
# df = my_spark.read.format("mongodb").load()

# 获取当前时间戳
current_timestamp = int(time.time())

# 计算过去七天的日期范围
start_timestamp = current_timestamp - 7 * 24 * 60 * 60
end_timestamp = current_timestamp

# 读取MongoDB数据集合
df = my_spark.read.format("mongodb").load()

# 过滤出过去七天的数据
df_filtered = df.filter((col("Timestamp") >= start_timestamp) & (col("Timestamp") < end_timestamp))

# 将时间戳转换为日期，并按日期分组统计每天的数据总量
df_stats = df_filtered.withColumn("date", date_format(from_unixtime(col("Timestamp") / 1000), "yyyy-MM-dd")) \
    .groupBy("date").count()

# 将统计结果转换为字典格式
statistics_dict = {row["date"]: row["count"] for row in df_stats.collect()}
print(statistics_dict)

# 将结果发送到WebSocket连接
@app.websocket("/websocket_cluster_device_status")
async def send_statistics_to_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(json.dumps(statistics_dict))
            await asyncio.sleep(10)
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await websocket.close()

# 关闭SparkSession
my_spark.stop()


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