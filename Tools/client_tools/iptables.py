import asyncio

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


async def block_ip(ip_address, domain_name):
    rule_name = f"Block {domain_name}"
    check_cmd = f"netsh advfirewall firewall show rule name=\"{rule_name}\""

    # 创建子进程，但确保正确关闭
    process = await asyncio.create_subprocess_shell(
        check_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        stdout, stderr = await process.communicate()
        output = stdout.decode('cp936', errors='ignore')

        if rule_name in output:
            print(f"Rule '{rule_name}' already exists.")
        else:
            cmd = f"netsh advfirewall firewall add rule name=\"{rule_name}\" dir=out interface=any action=block remoteip={ip_address}"
            add_process = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            await add_process.communicate()  # 确保命令执行完成
            print(f"Blocked IP {ip_address} for domain {domain_name}")
    finally:
        # 等待原始进程退出
        if process.returncode is None:
            process.kill()
        await process.wait()


