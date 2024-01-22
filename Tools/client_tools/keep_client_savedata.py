import socket

import psutil
import time
from Tools.client_tools import get_loc_ip
from Tools.mongo_tools import mongo_link
# 记录上一次的连接信息
def get_doamin(ip):
    try:
        # Get the hostname from the IP address
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        # Return the original IP address if no hostname is found
        return ip

def keep_client_save_ip_now_log():
    db_now = mongo_link.mongo_link_database("DGA_IP_now")
    db_log = mongo_link.mongo_link_database("DGA_IP_log")
    db_now.delete_many({})
    db_log.delete_many({})
    last_connections = set()
    while True:
        # 获取当前的连接信息
        connections = set(get_loc_ip.select_conn_ipv4())
        # 找到新建立的连接
        new_connections = list(connections - last_connections)
        # 找到关闭的连接
        closed_connections = list(last_connections - connections)

        # 处理新建立的连接
        if new_connections:
            new_data = []
            print("发现新连接：", len(new_connections))
            for conn in new_connections:
                local_addr = f'{conn.laddr.ip}:{conn.laddr.port}'
                remote_addr = f'{conn.raddr.ip}:{conn.raddr.port}'
                status = conn.status
                data = {
                    "local_address": local_addr,
                    "remote_address": remote_addr,
                    "status": status,
                    "timestamp":(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 添加一个时间戳字段
                }
                new_data.append(data)

            db_now.insert_many(new_data)
            db_log.insert_many(new_data)

        # 处理关闭的连接
        if closed_connections:
            delete_data = []
            print("连接已关闭：", len(closed_connections))
            for conn in closed_connections:
                local_addr = f'{conn.laddr.ip}:{conn.laddr.port}'
                remote_addr = f'{conn.raddr.ip}:{conn.raddr.port}'
                delete_data.append({"local_address": local_addr, "remote_address": remote_addr})
            db_now.delete_many({"$or": delete_data})

        # 更新上一次的连接信息
        last_connections = connections

        # 等待一段时间后再次检查连接信息
        time.sleep(1)
