from kafka import KafkaConsumer
import websockets
import socket
import asyncio
# 创建消费者，指定Kafka服务器地址和主题
consumer = KafkaConsumer('network_connections',
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
    uri = f'ws://{serverIp}/lisen'
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            print("Data sent to WebSocket:"+message)
    except Exception as e:
        print("Failed to send message via WebSocket:", e)

async def consume_messages():
    message_count = 0
    for _ in consumer:
        message_count += 1
        await send_to_websocket(str(message_count))

async def consume_and_send_messages(serverIp, consumer):
    uri = f'ws://{serverIp}/lisen'
    try:
        async with websockets.connect(uri) as websocket:
            message_count = 0
            for _ in consumer:
                message_count += 1
                await websocket.send(str(message_count))
                print("Data sent to WebSocket:" + str(message_count))
    except Exception as e:
        print("Failed to send message via WebSocket:", e)
# 启动异步主程序
asyncio.run(consume_messages())