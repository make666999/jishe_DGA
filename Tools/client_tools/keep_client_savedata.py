import socket
from queue import Queue
import time
from Tools.client_tools import get_loc_ip
from Tools.mongo_tools import mongo_link
import threading
from concurrent.futures import ThreadPoolExecutor
# 记录上一次的连接信息
content_queue = Queue()
db_now = mongo_link.mongo_link_database("DGA_IP_now")
db_log = mongo_link.mongo_link_database("DGA_IP_log")
def get_domain(ip):
    try:
        # Get the hostname from the IP address
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        # Return the original IP address if no hostname is found
        return ip
def process_connection(conn):
    remote_addr = f'{conn.raddr.ip}:{conn.raddr.port}'
    status = conn.status
    domain = get_domain(conn.raddr.ip)
    if domain != conn.raddr.ip:
        data = {
            "remote_address": remote_addr,
            "remote_domain": domain,
            "status": status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        content_queue.put(data)

def keep_client_save_ip_now_log():

    db_now = mongo_link.mongo_link_database("DGA_IP_now")
    db_log = mongo_link.mongo_link_database("DGA_IP_log")
    db_now.delete_many({})
    db_log.delete_many({})
    last_connections = set()
    executor = ThreadPoolExecutor(max_workers=10)
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
                executor.submit(process_connection, conn)
            while not content_queue.empty():
                item = content_queue.get()
                db_now.insert_one(item)
                db_log.insert_one(item)

        # 处理关闭的连接
        if closed_connections:
            delete_data = []
            print("连接已关闭：", len(closed_connections))
            for conn in closed_connections:

                remote_addr = f'{conn.raddr.ip}:{conn.raddr.port}'
                delete_data.append({ "remote_address": remote_addr})
            db_now.delete_many({"$or": delete_data})

        # 更新上一次的连接信息
        last_connections = connections

        # 等待一段时间后再次检查连接信息
        time.sleep(1)
