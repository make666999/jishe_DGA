│── main.py：系统运行总程序，异步调用get_domain函数

│
├── Model

│   ├── Data

│   │   ├── processing_2.py

│   │   ├── processing_class.py

│   │   ├── city_db
│   │   │   └── GeoLite2-City.mmdb
│   │   ├── clean_data
│   │   │   └── data_all.csv
│   │   └── Data-clean
│   │       ├── dga-domain.txt
│   │       └── top-1m.csv
│   ├── Model_File
│   │   └── Transformer+R_SKNET.pth
│   └── Train_Model
│       ├── Train_Transformer_R_SKNET.py
│       ├── log
│       │   └── Transformer+R_SKNET.csv
│       └── png
│           └── Transformer+R_SKNET.png
│
├── Tools
│   ├── client_tools
│   │   ├── get_domain.py：用于捕获和处理 DNS 数据包的异步程序，分析 DNS 查询和响应，根据预测模型和地理位置信息对域名进行分类和记录
│   │   └── get_loc_ip.py：获取系统的网络连接信息，筛选出其中的 IPv4 地址连接列表
│   ├── database_tools
│   │   └── dababase_use.py：获取当前机器的 IP 地址信息，并根据 IP 地址解析出其地理位置，将所得信息存储到 MongoDB 数据库
│   └── model_use_tools
│       └── predict_domain.py：用于域名分类预测的模型加载和预测函数
│
└── web_url
    ├── app.py：运行系统ui界面
    └── templates
        └── static
