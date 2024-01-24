
import time
from concurrent.futures import ThreadPoolExecutor


from scapy.all import sniff
from scapy.layers.dns import DNS

from Tools.database_tools import dababase_use
from Tools.model_use_tools import predict_domain

db_log = dababase_use.mongo_link_log()

model=predict_domain.Predict_Domain()

def process_connection(domain, type, ip=None):
    domain = domain.decode("utf-8").strip(".")
    converted_domain = predict_domain.predict_domain(model,domain)
    loc=dababase_use.get_ip_loc(ip)
    data = {
        "DNS_Type": type,
        "Remote_Address": ip,
        "Remote_Domain": domain,
        "Domain_Type": converted_domain,
        "Loc_Data": loc,
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    db_log.insert_one(data)
    print("新增数据：", data)


def dns_callback(packet):
    if packet.haslayer(DNS):

        dns = packet[DNS]
        for i in range(dns.ancount):
            dnsrr = dns.an[i]
            src_domain = dnsrr.rrname
            if dnsrr.type == 1 or dnsrr.type == 28:

                process_connection(src_domain, "response", dnsrr.rdata)
            else:
                continue
        else:
            return


def Get_Domain_Save():
    sniff(filter="port 53", prn=dns_callback, store=0)


def Get_Domain_Save_Main():
    executor = ThreadPoolExecutor(max_workers=10)
    executor.submit(Get_Domain_Save)
