import psutil


# 获取系统的网络连接信息，筛选IPv4地址的列表

def select_conn_ipv4():
    connections = psutil.net_connections()
    ipv4_addresses_conn = []
    for conn in connections:
        # 解析连接的远程IP地址
        if conn.raddr!=()and conn.raddr[0]!="127.0.0.1":
            remote_ip = conn.raddr[0]

            # 检查是否为IPv4地址
            if isinstance(remote_ip, str) and ':' not in remote_ip:
                # 将IPv4地址添加到列表中
                ipv4_addresses_conn.append(conn)
    return ipv4_addresses_conn

