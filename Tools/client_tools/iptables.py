import asyncio

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


def block_ip_new(ip_address: str, domain_name: str) -> None:
    """
    在 Windows 防火墙中添加一条出站阻止规则，用于封锁指定 IP。
    如果规则已存在，则直接提示，无需重复添加。

    :param ip_address: 需要封锁的远程 IP 地址
    :param domain_name: 规则中用于标识的域名（仅作备注）
    """
    rule_name = f"Block {domain_name}"
    check_cmd = ["netsh", "advfirewall", "firewall", "show", "rule", f"name={rule_name}"]

    # 查询规则是否已存在
    result = subprocess.run(check_cmd, capture_output=True, text=True, encoding="cp936", errors="ignore")

    if rule_name in result.stdout:
        # print(f"Rule '{rule_name}' already exists.")
        return

    # 添加防火墙规则
    add_cmd = [
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name={rule_name}", "dir=out", "interface=any",
        "action=block", f"remoteip={ip_address}"
    ]
    subprocess.run(add_cmd, check=True)
    # print(f"Blocked IP {ip_address} for domain {domain_name}")