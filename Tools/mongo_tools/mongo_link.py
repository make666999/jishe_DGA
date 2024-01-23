from pymongo import MongoClient

# 创建 MongoClient 对象，指定 MongoDB 的数据库、集合
def mongo_link_database(database_name):
    client = MongoClient("mongodb://8c630x9121.goho.co:23593")
    # 选择数据库
    db = client["WEB_TEST"]
    # 选择集合
    collection = db[database_name]
    return collection

