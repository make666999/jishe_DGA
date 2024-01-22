from Tools.mongo_tools import mongo_link

if __name__ == '__main__':
    db= mongo_link.mongo_link_database("DGA")
    res=db.insert_one({"URL": "www,baidu.com", "type": "True"})
    print("插入成功，文档ID：", res.inserted_id)
    documents = db.find()
    # 打印每个文档
    for doc in documents:
        print(doc)

