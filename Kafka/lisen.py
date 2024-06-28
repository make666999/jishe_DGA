from kafka import KafkaConsumer
import websockets
import socket
import asyncio
# 创建消费者，指定Kafka服务器地址和主题
consumer = KafkaConsumer('processed_dns_data',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest')

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Error occurred:", e)
        return None

serverIp = get_local_ip() + ":8000"
async def send_to_websocket(message):
    uri = f'ws://{serverIp}/lisen'  # 修改为你的WebSocket地址
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            print("Data sent to WebSocket")
    except Exception as e:
        print("Failed to send message via WebSocket:", e)

async def consume_messages():
    for message in consumer:
        await send_to_websocket(message.value.decode('utf-8'))
        print(f"Received message: {message.value.decode('utf-8')}")

# 运行消费者处理函数
asyncio.run(consume_messages())