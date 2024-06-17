import asyncio
import json
import time
import datetime
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from concurrent.futures import ThreadPoolExecutor
from pyspark.sql.functions import col, from_unixtime, date_format, last, countDistinct, first, count as sql_count, \
    struct, count
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
client = AsyncIOMotorClient("mongodb://127.0.0.1")
db = client["DGA"]
new_db = client["Data_pro"]


end_day = 20
# 当前时间的秒级时间戳
current_timestamp = int(time.time())
# 计算过去七天的起始时间戳
start_timestamp = current_timestamp - end_day * 24 * 60 * 60
# 结束时间戳应该是当前时间的前一天的23:59:59
end_timestamp = current_timestamp - 1

def week_data_any(df):


    df_filtered = df.filter((col("Timestamp")/1000 >= start_timestamp) & (col("Timestamp")/1000 <= end_timestamp))
    # 将毫秒级时间戳转换为日期并添加到新列 "date"
    df_filtered = df_filtered.withColumn("date", date_format(from_unixtime(col("Timestamp") / 1000), "yyyy-MM-dd"))

    statistics_dict_domain=domain_type(df_filtered)
    statistics_dict = data_all(df_filtered)



    # 计算每个集合中 Loc_Address 列的最后一个值
    last_loc_addresses = df_filtered.orderBy("date").agg(last("Loc_Address", True)).collect()
    last_loc_address = last_loc_addresses[0][0] if last_loc_addresses else None



    return statistics_dict, statistics_dict_domain,last_loc_address
def data_all(df_filtered):
    # 创建空统计字典
    statistics_dict_domain = {}
    current_date = datetime.now()
    for i in range(end_day - 1, 0, -1):  # 从前一天开始到前end_day天
        date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
        statistics_dict_domain[date] = 0  # 初始化为0

    # 对DataFrame按日期分组并计算每天的数据总量
    domain_date_counts = df_filtered.groupBy(col("date")).agg(count("*").alias("data_count")).collect()

    # 更新每天的数据计数
    for row in domain_date_counts:
        if row["date"] in statistics_dict_domain:  # 确保只更新已经初始化的键
            statistics_dict_domain[row["date"]] = row["data_count"]

    return statistics_dict_domain
def domain_type(df_filtered):
    statistics_dict_domain = {}

    # 获取当前时间并计算开始日期
    current_date = datetime.now()
    for i in range(end_day - 1, 0, -1):  # 从前一天开始到前end_day天
        date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
        statistics_dict_domain[date] = 0  # 初始化为0

    # 对每天的远程域名数量进行统计
    domain_date_counts = df_filtered.groupBy("date").agg(countDistinct("Remote_Domain").alias("domain_count")).collect()

    # 更新统计字典中的数量
    for row in domain_date_counts:
        if row["date"] in statistics_dict_domain:  # 确保只更新已经初始化的键
            statistics_dict_domain[row["date"]] = row["domain_count"]

    return statistics_dict_domain


def all_data_any(df):
    # 根据 toName 进行分组，并计算每个组的数量
    to_name_stats = df.groupBy("moveLines.toName").agg(
        sql_count("moveLines.toName").alias("count"),  # 使用 count() 函数
        first("moveLines.coords").alias("coords")  # 使用 first() 函数获取第一个 coords
    )

    # 过滤掉 toName 为 None 的行
    to_name_stats = to_name_stats.filter(col("toName").isNotNull())

    # 将结果转换为所需的格式
    results = to_name_stats.collect()
    all_data = [{"name": row["toName"], "coords": row["coords"][1], "count": row["count"]} for row in results]
    return all_data

def all_data_any_midd(df):
    # 根据 toName 进行分组，并计算每个组的数量
    to_name_stats = df.groupBy("moveLines.fromName").agg(
        sql_count("moveLines.fromName").alias("count"),  # 使用 count() 函数
        first("moveLines.coords").alias("coords")  # 使用 first() 函数获取第一个 coords
    )

    # 过滤掉 toName 为 None 的行
    to_name_stats = to_name_stats.filter(col("fromName").isNotNull())

    # 将结果转换为所需的格式
    results = to_name_stats.collect()
    all_data = [{"name": row["fromName"], "coords": row["coords"][0], "count": row["count"]} for row in results]
    return all_data
def dns_address_statistics(df):
    # 筛选出非空的 DNS_Address 字段
    df_filtered = df.filter(col("DNS_Address") != " ")

    # 对 DNS_Address 进行分组统计
    dns_type_counts = df_filtered.groupBy("DNS_Address").count()

    # 将结果收集到驱动器中
    dns_statistics = dns_type_counts.collect()

    # 转换为字典格式以便输出或进一步处理
    statistics_dict = {row['DNS_Address']: row['count'] for row in dns_statistics}

    return statistics_dict
def analyze_domain_type_counts(df):
    # 对 `Domain_Type` 字段进行分组并计数
    domain_type_counts = df.groupBy("Domain_Type").count()

    # 选择并重命名列，以便输出更加直观
    result_df = domain_type_counts.select(
        col("Domain_Type").alias("Domain_Type"),
        col("count").alias("Count")
    )
    results = result_df.collect()
    result_dicts = [{"Domain_Type": row["Domain_Type"], "Count": row["Count"]} for row in results]
    return result_dicts


def analyze_traffic_by_route_with_coords(df):
    traffic_counts = df.groupBy(col("moveLines.fromName").alias("fromName"),
                                col("moveLines.toName").alias("toName")).count()

    # 选择并重命名列，使输出更具可读性
    result_df = traffic_counts.select(
        col("fromName").alias("From_Name"),
        col("toName").alias("To_Name"),
        col("count").alias("Traffic_Count")
    ).orderBy(col("Traffic_Count").desc())

    # 收集结果为字典列表
    results = result_df.collect()
    result_dicts = [{"route": [row["From_Name"], row["To_Name"]], "Count": row["Traffic_Count"]} for row in
                    results]

    return result_dicts


def read_and_count_collection(collection_name):

    # 读取MongoDB数据
    df = my_spark.read \
        .format("mongodb") \
        .option("database", "DGA") \
        .option("collection", collection_name) \
        .load()
    statistics_dict,statistics_dict_domain,last_loc_address=week_data_any(df)
    dns_address_type=dns_address_statistics(df)
    map_data=all_data_any(df)
    DGA_type_analyze=analyze_domain_type_counts(df)
    analyze_traffic_by_route=analyze_traffic_by_route_with_coords(df)
    mid_dns_point=all_data_any_midd(df)
    data_week_totle = {
        "Device_Name": collection_name,
        "Week_Statistics": statistics_dict,
        "Week_Domain_all": statistics_dict_domain,
        "last_loc_address":last_loc_address,
        "map_data":map_data,
        "dns_address_type":dns_address_type,
        "DGA_type_analyze":DGA_type_analyze,
        "analyze_traffic_by_route_with_coords":analyze_traffic_by_route,
        "mid_dns_point":mid_dns_point
    }

    print(data_week_totle)
    with open('data_total.json', 'w', encoding='utf-8') as f:

        json.dump(data_week_totle, f, ensure_ascii=False, indent=4)
    return data_week_totle


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
