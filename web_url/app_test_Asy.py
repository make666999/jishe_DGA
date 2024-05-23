import asyncio
import time
import datetime
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from concurrent.futures import ThreadPoolExecutor
from pyspark.sql.functions import col, from_unixtime, date_format
from pyspark.sql import SparkSession


# 创建SparkSession并配置MongoDB连接
my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.read.connection.uri", "mongodb://886xt49626.goho.co:23904") \
    .config("spark.mongodb.write.connection.uri", "mongodb://886xt49626.goho.co:23904") \
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
    .getOrCreate()


# 创建异步MongoDB客户端
client = AsyncIOMotorClient("mongodb://886xt49626.goho.co:23904")
db = client["DGA"]


current_timestamp = int(time.time())
# 计算过去七天的时间戳范围
start_timestamp = current_timestamp - 7 * 24 * 60 * 60
end_timestamp = current_timestamp

# 存储统计结果的字典，以日期为键，数据量为值
statistics_dict = {}
# 定义一个同步函数用于读取集合数据并统计行数
def read_and_count_collection(collection_name):

        # 读取MongoDB数据
        df = my_spark.read \
            .format("mongodb") \
            .option("database", "DGA") \
            .option("spark.mongodb.read.connection.uri", "mongodb://886xt49626.goho.co:23904") \
            .option("spark.mongodb.write.connection.uri", "mongodb://886xt49626.goho.co:23904") \
            .option("collection", collection_name) \
            .load()

        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            statistics_dict[date] = 0

        df_filtered = df.filter((col("Timestamp") >= start_timestamp) & (col("Timestamp") < end_timestamp))

        # 将时间戳转换为日期
        df_filtered = df_filtered.withColumn("date",
                                             date_format(from_unixtime(col("Timestamp") / 1000), "yyyy-MM-dd"))
        date_counts = df_filtered.groupBy("date").count().collect()
        for row in date_counts:
            date = row["date"]
            count = row["count"]
            statistics_dict[date] += count

        return statistics_dict


# 异步包装同步函数
async def async_read_and_count_collection(executor, collection_name):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, read_and_count_collection, collection_name)
    return result
async def send_week_data():
    try:
        # 初始化存储总行数的字典
        total_counts = {}
        # 获取数据库中的所有集合名称
        collection_names = await db.list_collection_names()
        # 创建ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            # 创建异步任务列表
            tasks = [async_read_and_count_collection(executor, name) for name in collection_names]

            # 并行执行任务
            results = await asyncio.gather(*tasks)



            # 遍历每个结果字典
            for result in results:
                # 遍历结果字典中的日期和对应的行数
                for date, count in result.items():
                    # 将行数累加到总行数中
                    total_counts[date] = total_counts.get(date, 0) + count




            print(f"DGA 数据库中所有集合的总行数: {total_counts}")


    finally:
        # 关闭MongoDB客户端
        return total_counts
        client.close()

# 运行异步任务
asyncio.run(send_week_data())
