
import time
from concurrent.futures import ThreadPoolExecutor


from scapy.all import sniff
from scapy.layers.dns import DNS
from scapy.layers.inet import IP

from Tools.database_tools import dababase_use
from Tools.model_use_tools import predict_domain

db_log = dababase_use.mongo_link_log()

model=predict_domain.Predict_Domain()

def process_connection(domain,dst_ip,loc_ip, type, domain_ip=None):
    domain = domain.decode("utf-8").strip(".")
    domain_type = predict_domain.predict_domain(model,domain)
    loc=dababase_use.get_ip_loc(domain_ip)

    data = {
        "DNS_Type": type,
        "Loc_Address": loc_ip,
        "DNS_Address": dst_ip,
        "Domain_Address": domain_ip,
        "Remote_Domain": domain,
        "Domain_Type": domain_type,
        "Loc_Data": loc,
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    db_log.insert_one(data)
    print("\n[*] 新增连接: %s <- %s - 解析域名: %s : %s - 域名检查结果: %s - 时间: %s" % (
        dst_ip, loc_ip, domain, domain_ip,domain_type,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def dns_callback(packet):
    if packet.haslayer(DNS):

        dns = packet[DNS]
        for i in range(dns.ancount):
            dnsrr = dns.an[i]
            src_domain = dnsrr.rrname
            if dnsrr.type == 1 or dnsrr.type == 28:

                process_connection(src_domain,packet[IP].dst,packet[IP].src, "response", dnsrr.rdata)
            else:
                continue
        else:
            return


def Get_Domain_Save():
    sniff(filter="port 53", prn=dns_callback, store=0,iface="以太网")


def Get_Domain_Save_Main():
    executor = ThreadPoolExecutor(max_workers=10)
    executor.submit(Get_Domain_Save)
