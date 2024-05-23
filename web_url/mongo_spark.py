import asyncio
import json
from pyspark.sql.types import StructType, StructField, StringType, MapType, LongType

import time
import datetime
from datetime import datetime, timedelta
from pyspark.sql.functions import first, last
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from concurrent.futures import ThreadPoolExecutor
from pyspark.sql.functions import col, from_unixtime, date_format
from pyspark.sql import SparkSession

# 创建SparkSession并配置MongoDB连接
my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1") \
    .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.13:10.3.0") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .config("spark.sql.shuffle.partitions", "400") \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.cores", "2") \
    .config("spark.kryoserializer.buffer.max", "512m") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.network.timeout", "600s") \
    .config("spark.executor.heartbeatInterval", "60s") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "false")\
    .getOrCreate()

# 创建异步MongoDB客户端
client = AsyncIOMotorClient("mongodb://886xt49626.goho.co:23904")
db = client["DGA"]
new_db = client["Data_pro"]

end_timestamp = int(time.time())
# 计算过去七天的时间戳范围
start_timestamp = 1000 * (end_timestamp - 8 * 24 * 60 * 60)
end_timestamp = 1000 * (end_timestamp - 1 * 24 * 60 * 60)



# 定义一个同步函数用于读取集合数据并统计行数
def read_and_count_collection(collection_name):
    statistics_dict = {}
    for i in range(1,8):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        statistics_dict[date] = 0
    # 读取MongoDB数据
    df = my_spark.read \
        .format("mongodb") \
        .option("database", "DGA") \
        .option("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1") \
        .option("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1") \
        .option("collection", collection_name) \
        .load()

    df_filtered = df.filter((col("Timestamp") >= start_timestamp) & (col("Timestamp") <= end_timestamp))

    # 将毫秒级时间戳转换为日期并添加到新列 "date"
    df_filtered = df_filtered.withColumn("date", date_format(from_unixtime(col("Timestamp") / 1000), "yyyy-MM-dd"))

    date_counts = df_filtered.groupBy("date").count().collect()


    # 计算每个集合中 Loc_Address 列的最后一个值
    last_loc_addresses = df_filtered.orderBy("date").agg(last("Loc_Address", True)).collect()
    last_loc_address = last_loc_addresses[0][0] if last_loc_addresses else None

    # 将date_counts的值存入statistics_dict，并一一匹配
    for row in date_counts:
        statistics_dict[row["date"]] = row["count"]
    data = {
        "Device_Name": collection_name,
        "Week_Statistics": statistics_dict,
        "last_loc_address":last_loc_address
    }
    print(data)
    return data


# 异步包装同步函数
async def async_read_and_count_collection(executor, collection_name):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, read_and_count_collection, collection_name)
    return result

async def update_document(collection, result):
    await collection.update_one(
        {"Device_Name": result["Device_Name"]},
        {"$set": result},
        upsert=True
    )

async def send_week_data():
    try:
        # 获取数据库中的所有集合名称
        collection_names = await db.list_collection_names()
        # 创建ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            # 创建异步任务列表
            tasks = [async_read_and_count_collection(executor, name) for name in collection_names]

            # 并行执行任务
            results = await asyncio.gather(*tasks)

            test_collection = new_db["test"]

            # 创建异步任务列表，更新数据
            update_tasks = [update_document(test_collection, result) for result in results]
            # 并行执行更新操作
            await asyncio.gather(*update_tasks)
    finally:
        # 关闭MongoDB客户端
        client.close()


# 运行异步任务
asyncio.run(send_week_data())
