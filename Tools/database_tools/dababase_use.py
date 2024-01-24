import os
from pymongo import MongoClient
import geoip2.database
# 创建 MongoClient 对象，指定 MongoDB 的数据库、集合

# reader_path = os.path.abspath(os.path.join(".","Model", "Data","city_db", "GeoLite2-City.mmdb"))
reader_path="./Model/Data/city_db/GeoLite2-City.mmdb"
reader=geoip2.database.Reader(reader_path)
def mongo_link_database(database_name):
    client = MongoClient("mongodb://8c630x9121.goho.co:23593")
    # 选择数据库
    db = client["DGA"]
    # 选择集合
    collection = db[database_name]
    return collection
def mongo_link_log():
    return mongo_link_database("DGA_Domain_Log")

def get_ip_loc(ip):
    try:
        response = reader.city(ip)
        data= {
            "city":response.city.names["zh-CN"],
            "x":response.location.latitude,
            "y":response.location.longitude
        }
    except:
        return None
    return data
