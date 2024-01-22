from pymongo import MongoClient

# 创建 MongoClient 对象，指定 MongoDB 的连接地址和端口号
def mongo_link_database():
    client = MongoClient("mongodb://8c630x9121.goho.co:23593")

    # 选择数据库
    db = client["test"]

    # 选择集合
    collection = db["DGA"]
    return collection
    # # 插入文档
    # document = {"URL": "www.baidu.com", "type": "True"}
    # result = collection.insert_one(document)
    # print("插入成功，文档ID：", result.inserted_id)
    #
    # # 查询文档
    # query = {"URL": "www.baidu.com"}
    # result = collection.find(query)
    # for document in result:
    #     print(document)

# # 关闭连接
# client.close()
