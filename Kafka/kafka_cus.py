import asyncio
import time
import faust
import json

from kafka import KafkaProducer

from Tools.database_tools import database_use
from Tools.model_use_tools import predict_domain

db_log = database_use.mongo_link_log()
model = predict_domain.Predict_Domain()
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

async def process_connection(domain, dst_ip, loc_ip, type, domain_ip=None):
    loop = asyncio.get_running_loop()
    domain = domain.strip(".")  # 直接处理字符串
    domain_type = await loop.run_in_executor(None, predict_domain.predict_domain, model, domain)
    loc = await loop.run_in_executor(None, database_use.get_ip_loc, domain_ip)

    data = {
        "DNS_Type": type,
        "Loc_Address": dst_ip,
        "DNS_Address": loc_ip,
        "Domain_Address": domain_ip,
        "Remote_Domain": domain,
        "Domain_Type": domain_type,
        "moveLines": loc,
        "Timestamp": int(time.time() * 1000)
    }
    producer.send('processed_dns_data', value=data)
    producer.flush()
    print(f"\n[*] 数据推送到Kafka完成: {data}")
    await loop.run_in_executor(None, db_log.insert_one, data)
    print("\n[*] 数据写入完成: %s <- %s - 解析域名: %s : %s - 域名检查结果: %s - 时间: %s" % (
        dst_ip, loc_ip, domain, domain_ip, domain_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

app = faust.App('hello-world', broker='kafka://localhost:9092', value_serializer='raw')
greetings_topic = app.topic('dns_topic')

@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        # 解析消息，假设消息是JSON格式的字符串
        data = json.loads(greeting)
        # 提取数据
        domain = data[0]
        dst_ip = data[1]
        loc_ip = data[2]
        type = data[3]
        domain_ip = data[4]

        await process_connection(
            domain=domain,
            dst_ip=dst_ip,
            loc_ip=loc_ip,
            type=type,
            domain_ip=domain_ip
        )
