import pydivert
def intercept_domain_traffic(domain):
    filter_rule = "tcp.PayloadLength > 0 and (tcp.DstPort == 80 or tcp.DstPort == 443)"
    with pydivert.WinDivert(filter_rule) as w:
        print(f"开始拦截包含域名 {domain} 的网络流量。")
        domain_bytes = domain.encode()

        for packet in w:
            if domain_bytes in packet.payload:
                print(f"拦截到域名请求: {domain}")
                continue
            else:
                # 如果数据包负载不包含指定域名，正常发送数据包
                w.send(packet, recalculate_checksum=True)
import subprocess

def block_ip(ip_address, domain_name):
    rule_name = f"Block {domain_name}"
    # 添加防火墙规则
    cmd = f"netsh advfirewall firewall add rule name=\"{rule_name}\" dir=out interface=any action=block remoteip={ip_address}"
    subprocess.run(cmd, shell=True)
    print(f"Blocked IP {ip_address} for domain {domain_name}")


