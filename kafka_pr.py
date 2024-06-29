from kafka import KafkaProducer
import json
from scapy.all import sniff
from scapy.layers.dns import DNS
from scapy.layers.inet import IP

def create_producer():
    return KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

producer = create_producer()

def dns_callback(packet):
    try:
        if packet.haslayer(DNS):
            dns = packet[DNS]
            for i in range(dns.ancount):
                dnsrr = dns.an[i]
                src_domain = dnsrr.rrname
                if dnsrr.type == 1 or dnsrr.type == 28:
                    message = [str(src_domain), packet[IP].dst, packet[IP].src, "response", dnsrr.rdata]
                    print(message)
                    producer.send('dns_topic', message)
    except Exception as e:
        print("error:", e)

def sniff_dns():
    sniff(filter="port 53", prn=dns_callback, store=0, iface="以太网")

if __name__ == "__main__":
    sniff_dns()
