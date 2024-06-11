import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# 连接到MongoDB
client = AsyncIOMotorClient("mongodb://886xt49626.goho.co:23904")
db = client["Data_pro"]
collection = db["test"]

# 定义添加新列的异步函数
async def add_new_column():
    # 使用update_many来更新所有文档
    await collection.update_many(
        {},  # 更新所有文档
        {'$set': {'model': '00'}}  # 添加的新列和默认值
    )
    print("All documents updated with new column.")

# 运行异步函数
asyncio.run(add_new_column())

# 关闭MongoDB客户端
client.close()
