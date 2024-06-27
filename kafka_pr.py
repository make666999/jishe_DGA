from kafka import KafkaProducer
import json
from scapy.all import sniff
from scapy.layers.dns import DNS
from scapy.layers.inet import IP

from Tools.database_tools import database_use
from Tools.model_use_tools import predict_domain

def create_producer():
    return KafkaProducer(
        bootstrap_servers='localhost:9092',  # Kafka集群地址，如果有多个节点，使用逗号分隔
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 序列化发送的消息为JSON格式
    )

producer = create_producer()

def dns_callback(packet):
    try:
        if packet.haslayer(DNS):
            dns = packet[DNS]
            for i in range(dns.ancount):
                dnsrr = dns.an[i]
                src_domain = dnsrr.rrname
                if dnsrr.type == 1 or dnsrr.type == 28:  # Check for A and AAAA records
                    message = [str(src_domain), packet[IP].dst, packet[IP].src, "response", dnsrr.rdata]
                    print(message)  # 打印消息用于调试
                    producer.send('dns_topic', message)
    except Exception as e:
        print("error:", e)

def sniff_dns():
    sniff(filter="port 53", prn=dns_callback, store=0, iface="以太网")

if __name__ == "__main__":
    sniff_dns()
