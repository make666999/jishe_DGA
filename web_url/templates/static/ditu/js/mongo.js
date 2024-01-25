const { MongoClient } = require('mongodb');

async function main() {
  // MongoDB连接URL
  const uri = "mongodb://8c630x9121.goho.co:23593";
  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

  try {
    // 连接到MongoDB服务器
    await client.connect();
    console.log("成功连接到数据库");

    // 指定数据库和集合
    const database = client.db("DGA");
    const collection = database.collection("GPU-SERVER");

    // 查找集合中的文档并打印
    const documents = await collection.find({}).toArray();
    console.log("集合中的文档:", documents);
  } catch (e) {
    console.error("数据库操作出错:", e);
  } finally {
    // 关闭数据库连接
    await client.close();
  }
}

main().catch(console.error);
