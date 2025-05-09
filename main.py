import asyncio
import socket

from pymongo import MongoClient
import kafka_pr
from Tools.client_tools import get_domain
from uvicorn import run

mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
hostname = socket.gethostname()
if __name__ == '__main__':
    db2 = mongo_client["Data_pro"]
    collection = db2["test"]
    document = collection.find_one({"Device_Name": hostname})
    model = document["model"]  # 假设是 "102002"

    part = model[:2]
    flag = model[2]
    control_map = {
        "0": (False, False, False),
        "1": (True, True, False),
        "2": (True, True, True),
    }
    try:
        use_kafka, use_redis, enable_block = control_map[flag]
    except KeyError:
        raise ValueError(f"未知的控制标志位: {flag}")

    if part=="00":
        asyncio.run(get_domain.main(use_kafka=use_kafka,
        use_redis=use_redis,
        enable_block=enable_block,))
    elif part=="01" or part=="02":
        kafka_pr.sniff_dns()






    #获得当前主机建立的连接、IP访问日志（log）、维持实时会话表（now）



