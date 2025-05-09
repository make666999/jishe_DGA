"""
redis_to_mongo_worker.py
---------------------------------
Redis Streams → MongoDB 同步 Worker（Write‑Behind）

- 从 Redis Stream `mongo_write_stream` 读取数据
- 写入 MongoDB（motor 异步驱动）
- 成功后 XACK + XDEL，失败保持 pending 以便后续重试

依赖安装：
```bash
pip install redis motor
```
"""

import asyncio
import json
import os
import signal
import socket
from typing import Any

import redis.asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient
hostname = socket.gethostname()
# ---------------- 配置 ----------------
STREAM_KEY = "dns_connections"
GROUP_NAME = "dns_consumers"             # Consumer Group 名称
CONSUMER_ID = f"{socket.gethostname()}-{os.getpid()}"  # 本 Worker 的唯一 ID

REDIS_URL = "redis://localhost:6379/0"     # Redis 连接串
MONGO_URL = "mongodb://localhost:27017"     # MongoDB 连接串
MONGO_DB = "DGA"                            # MongoDB 数据库
MONGO_COL = hostname                      # MongoDB 集合

BATCH = 100       # 每次最多读取多少条消息
BLOCK_MS = 5000   # XREADGROUP 阻塞时长（毫秒）
# --------------------------------------


class RedisMongoSync:
    """Redis Streams → MongoDB 的异步同步 Worker"""

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.redis: aioredis.Redis | None = None
        self.mongo = AsyncIOMotorClient(MONGO_URL)[MONGO_DB][MONGO_COL]
        self._stop_event = asyncio.Event()

    # ---------- 初始化 ----------
    async def _init_redis(self):
        self.redis = aioredis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
        # 若 Group 已存在会抛 BUSYGROUP，忽略即可
        try:
            await self.redis.xgroup_create(
                name=STREAM_KEY,
                groupname=GROUP_NAME,
                id="$",
                mkstream=True,
            )
        except aioredis.ResponseError as exc:
            if "BUSYGROUP" not in str(exc):
                raise

    # ---------- 主循环 ----------
    async def run(self):
        await self._init_redis()
        print("[Worker] Started Redis → MongoDB sync …")
        while not self._stop_event.is_set():
            try:
                results = await self.redis.xreadgroup(
                    groupname=GROUP_NAME,
                    consumername=CONSUMER_ID,
                    streams={STREAM_KEY: ">"},  # 只取新消息
                    count=BATCH,
                    block=BLOCK_MS,
                )
                if not results:
                    continue  # 超时，继续下一轮

                for _stream, msgs in results:
                    for msg_id, fields in msgs:
                        await self._handle_message(msg_id, fields)
            except Exception as exc:
                print("[Worker] Loop error:", exc)
                await asyncio.sleep(5)

    # ---------- 处理单条消息 ----------
    async def _handle_message(self, msg_id: str, fields: dict[str, Any]):
        try:
            payload = json.loads(fields["data"])

            # 写入 MongoDB（insert_one 默认异步）
            await self.mongo.insert_one(payload)
            # ACK & 删除，防止 Stream 无限增长
            await self.redis.xack(STREAM_KEY, GROUP_NAME, msg_id)
            await self.redis.xdel(STREAM_KEY, msg_id)
            print("[Worker] Received message: ", payload["Remote_Domain"]+" Domain_Type : " +payload["Domain_Type"])
        except Exception as exc:
            # 失败时不 ACK，让消息留在 Pending List 以便稍后重试
            print("[Worker] Mongo write failed:", exc, "msg_id:", msg_id)

    # ---------- 关闭 ----------
    async def close(self):
        self._stop_event.set()
        if self.redis is not None:
            await self.redis.close()
        self.mongo.database.client.close()
        print("[Worker] Shutdown complete.")


async def main():
    worker = RedisMongoSync()


    def _graceful_shutdown(*_):
        asyncio.create_task(worker.close())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            asyncio.get_running_loop().add_signal_handler(sig, _graceful_shutdown)
        except NotImplementedError:  # Windows 无法注册 SIGTERM
            pass
    # --------------------------------

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
