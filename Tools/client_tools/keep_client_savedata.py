import psutil
import time
import get_loc_ip
from Tools.mongo_tools import mongo_link
# 记录上一次的连接信息
last_connections = []
#连接数据库
db= mongo_link.mongo_link_database("DGA")

while True:
    # 获取当前的连接信息
    connections = get_loc_ip.select_conn_ipv4()

    # 找到新建立的连接
    new_connections = [conn for conn in connections if conn not in last_connections]

    # 找到关闭的连接
    closed_connections = [conn for conn in last_connections if conn not in connections]

    # 处理新建立的连接
    if new_connections:
        print("发现新连接：", new_connections)
        for conn in new_connections:
            local_addr = f'{conn.laddr.ip}:{conn.laddr.port}'
            remote_addr = f'{conn.raddr.ip}:{conn.raddr.port}'
            status = conn.status
            data = {
                "local_address": local_addr,
                "remote_address": remote_addr,
                "status": status,
                "timestamp": int(time.time())  # 添加一个时间戳字段
            }
            db.insert_one(data)

    # 处理关闭的连接
    if closed_connections:
        print("连接已关闭：", closed_connections)
        for conn in closed_connections:
            local_addr = f'{conn.laddr.ip}:{conn.laddr.port}'
            remote_addr = f'{conn.raddr.ip}:{conn.raddr.port}'
            db.delete_one({"local_address": local_addr, "remote_address": remote_addr})

    # 更新上一次的连接信息
    last_connections = connections

    # 等待一段时间后再次检查连接信息
    time.sleep(1)
