import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor

import redis.asyncio as aioredis
from aiokafka import AIOKafkaProducer
from scapy.all import sniff
from scapy.layers.dns import DNS
from scapy.layers.inet import IP

from Tools.client_tools.iptables import block_ip, block_ip_new
from Tools.database_tools import database_use
from Tools.model_use_tools import predict_domain

# ---------- Windows 环境建议 ----------
# aiokafka + Windows 最稳定的组合是 SelectorEventLoop
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# -------------------------------------

# ---------- 全局对象 ----------
redis_client: aioredis.Redis | None = None
kafka_producer: AIOKafkaProducer | None = None
main_loop: asyncio.AbstractEventLoop | None = None  # 主事件循环

# Redis Stream 相关常量
STREAM_KEY = "dns_connections"
GROUP_NAME = "dns_consumers"
# --------------------------------

# ---------- 业务依赖 ----------
db_log = database_use.mongo_link_log()
model = predict_domain.Predict_Domain()
# --------------------------------


# ========== 初始化外部连接 ==========
async def init_connections() -> None:
    """初始化 Redis、Kafka，并确保 Stream Group 存在."""
    global redis_client, kafka_producer, main_loop
    main_loop = asyncio.get_running_loop()

    # 1) Redis（redis-py 的 asyncio 客户端，内部自带连接池）
    redis_client = aioredis.from_url(
        "redis://localhost:6379/0",
        encoding="utf-8",
        decode_responses=True,
        max_connections=10,
    )

    # 确保 Stream & Group 存在
    try:
        await redis_client.xgroup_create(
            name=STREAM_KEY,
            groupname=GROUP_NAME,
            id="0-0",
            mkstream=True,
        )
        print(f"[*] Redis Stream 组已创建: {STREAM_KEY} / {GROUP_NAME}")
    except aioredis.ResponseError as e:
        # BUSYGROUP 说明已存在，忽略
        if "BUSYGROUP" in str(e):
            print(f"[*] Redis Stream 组已存在: {STREAM_KEY} / {GROUP_NAME}")
        else:
            raise

    # 2) Kafka Producer —— 不手动指定 loop，默认用当前主循环
    kafka_producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
    )
    await kafka_producer.start()
# ===================================


# ========== 核心处理协程 ==========
async def process_connection(
    domain: bytes,
    dst_ip: str,
    loc_ip: str,
    dns_type: str,
    domain_ip: str | None = None,
) -> None:
    """一次 DNS 解析记录的完整处理流程."""
    global redis_client, kafka_producer

    # 0) 解析域名并预测
    loop = asyncio.get_running_loop()
    domain_str = domain.decode("utf-8").strip(".")
    domain_type = await loop.run_in_executor(
        None, predict_domain.predict_domain, model, domain_str
    )
    loc = await loop.run_in_executor(None, database_use.get_ip_loc, domain_ip)
    # print(domain_type)
    # 1) 阻断恶意域名
    if domain_type != "BENIGN":
        await loop.run_in_executor(None,block_ip_new,domain_ip, domain_str)
        print(f"[!] 已阻止 {domain_str} ({domain_ip})，类型: {domain_type}")

    # 2) 构造统一数据结构
    data = {
        "DNS_Type": dns_type,
        "Loc_Address": dst_ip,
        "DNS_Address": loc_ip,
        "Domain_Address": domain_ip,
        "Remote_Domain": domain_str,
        "Domain_Type": domain_type,
        "moveLines": loc,
        "Timestamp": int(time.time() * 1000),
    }

    # 3) 写入 Redis Stream
    try:
        stream_id = await redis_client.xadd(
            STREAM_KEY, {"data": json.dumps(data)}
        )
        print(f"[*] Redis Stream <- {STREAM_KEY} {data}")
    except Exception as e:
        print("写 Redis Stream 出错：", e)

    # 4) 推送 Kafka
    try:
        await kafka_producer.send_and_wait(
            "network_connections", json.dumps(data).encode()
        )
        print("[*] Kafka <- network_connections")
    except Exception as e:
        print("推 Kafka 出错：", e)

    # 5) 写入 MongoDB
    await loop.run_in_executor(None, db_log.insert_one, data)
    print(
        f"[*] 完成: {dst_ip} <- {loc_ip}  {domain_str}({domain_ip})  {domain_type}"
    )
# ==================================


# ========== Scapy 抓包 ==========
def packet_handler(pkt) -> None:
    """同步回调：提取 DNS 记录并丢给主循环的协程处理."""
    if not pkt.haslayer(DNS):
        return

    dns_layer = pkt[DNS]
    ip_layer = pkt[IP]
    for i in range(dns_layer.ancount):
        try:
            dns_rr = dns_layer.an[i]
            # 只处理 A(1) / AAAA(28) 记录
            if dns_rr.type not in (1, 28):
                continue
            print(dns_rr.rrname,
                ip_layer.dst,
                ip_layer.src,
                "response",
                str(dns_rr.rdata))
            # 提交协程到主事件循环
            coro = process_connection(
                dns_rr.rrname,
                ip_layer.dst,
                ip_layer.src,
                "response",
                str(dns_rr.rdata),
            )
            asyncio.run_coroutine_threadsafe(coro, main_loop)
        except:
            pass

def sniff_dns() -> None:
    """在独立线程中执行的阻塞式抓包."""
    sniff(filter="port 53", prn=packet_handler, store=False, iface="WLAN")
# ===============================


# ========== 程序入口 ==========
async def main() -> None:
    """程序主入口：初始化，然后把 sniff 放到线程池里跑."""
    await init_connections()

    # 把 blocking 的 sniff 放线程池
    executor = ThreadPoolExecutor(max_workers=1)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, sniff_dns)


if __name__ == "__main__":
    asyncio.run(main())
