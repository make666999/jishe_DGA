
import requests
from pymongo import MongoClient
import geoip2.database
import socket
# 创建 MongoClient 对象，指定 MongoDB 的数据库、集合

# reader_path = os.path.abspath(os.path.join("Model", "Data","city_db", "GeoLite2-City.mmdb"))
reader_path="./Model/Data/city_db/GeoLite2-City.mmdb"
reader=geoip2.database.Reader(reader_path)
def get_ip():
    try:
        response = requests.get('http://ip-api.com/json/')

        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching IP: {e}")
        return None
ip_data=get_ip()

loc_city=ip_data['city']
loc_x_y=[ip_data["lon"],ip_data["lat"]]

def mongo_link_database(database_name):

    client = MongoClient("mongodb://nl86309121.vicp.fun:30786")
    # 选择数据库
    db = client["DGA"]
    # 选择集合
    collection = db[database_name]
    return collection
def mongo_link_log():
    hostname = socket.gethostname()
    return mongo_link_database(hostname)

def get_ip_loc(ip):
    try:
        response = reader.city(ip)
        data= {
            "fromName": loc_city,
            "toName":response.city.names["zh-CN"],
            "coords":[loc_x_y,[response.location.longitude,response.location.latitude]],
        }
    except:
        return None
    return data
