import asyncio
import random
import time
from random import choice


async def process_connection(domain, dst_ip, loc_ip, type):
    # 模拟网络请求和数据库响应的延迟
    await asyncio.sleep(random.uniform(0.05, 0.1))
    print(f"处理完成: {domain} -> {dst_ip}")


def linear_processing(dns_requests):
    for request in dns_requests:
        time.sleep(random.uniform(0.05, 0.1))  # 模拟处理时间
        print(f"线性处理: {request['domain']} -> {request['dst_ip']}")


async def concurrent_processing(dns_requests):
    tasks = [asyncio.create_task(
        process_connection(request['domain'], request['dst_ip'], request['loc_ip'], request['type']))
             for request in dns_requests]
    await asyncio.gather(*tasks)


def prepare_requests(num_requests=10):
    domains = ["example.com", "test.org", "demo.net", "sample.edu"]
    ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]
    requests = [
        {"domain": choice(domains), "dst_ip": choice(ips), "loc_ip": choice(ips), "type": "response"}
        for _ in range(num_requests)
    ]
    return requests


def measure_performance():
    dns_requests = prepare_requests(10)  # 生成10个DNS请求

    # 线性处理和并发处理的性能测试
    linear_times = []
    concurrent_times = []

    for _ in range(5):  # 运行5次来测量平均性能
        # 线性处理
        start_linear = time.time()
        linear_processing(dns_requests)
        end_linear = time.time()
        linear_times.append(end_linear - start_linear)

        # 异步并发处理
        start_concurrent = time.time()
        asyncio.run(concurrent_processing(dns_requests))
        end_concurrent = time.time()
        concurrent_times.append(end_concurrent - start_concurrent)

    # 计算平均时间
    avg_linear = sum(linear_times) / len(linear_times)
    avg_concurrent = sum(concurrent_times) / len(concurrent_times)

    print("Average linear processing time:", avg_linear)
    print("Average concurrent processing time:", avg_concurrent)


if __name__ == "__main__":
    measure_performance()
