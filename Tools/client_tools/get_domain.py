import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from scapy.all import sniff
from scapy.layers.dns import DNS
from scapy.layers.inet import IP

from Tools.database_tools import database_use
from Tools.model_use_tools import predict_domain

db_log = database_use.mongo_link_log()
model = predict_domain.Predict_Domain()


async def process_connection(domain, dst_ip, loc_ip, type, domain_ip=None):
    loop = asyncio.get_running_loop()
    domain = domain.decode("utf-8").strip(".")
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
    await loop.run_in_executor(None, db_log.insert_one, data)
    print("\n[*] 数据写入完成: %s <- %s - 解析域名: %s : %s - 域名检查结果: %s - 时间: %s" % (
        dst_ip, loc_ip, domain, domain_ip, domain_type, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


async def dns_callback(packet):
    try:
        if packet.haslayer(DNS):
            dns = packet[DNS]
            tasks = []
            for i in range(dns.ancount):
                dnsrr = dns.an[i]
                src_domain = dnsrr.rrname
                if dnsrr.type == 1 or dnsrr.type == 28:
                    task = asyncio.create_task(
                        process_connection(src_domain, packet[IP].dst, packet[IP].src, "response", dnsrr.rdata))
                    tasks.append(task)
                else:
                    continue
            if tasks:
                await asyncio.gather(*tasks)
    except:
        print("error")

def sniff_dns():
    sniff(filter="port 53", prn=lambda x: asyncio.run(dns_callback(x)), store=0, iface="以太网 4")


async def main():
    executor = ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_running_loop()
    loop.set_default_executor(executor)
    await loop.run_in_executor(None, sniff_dns)

