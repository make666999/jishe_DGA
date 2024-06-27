# 项目文件结构

## main.py
- 单一启动本机域名检测服务的主入口脚本

## Model
- 包含所有与数据处理和模型训练相关的文件。
- 包含模型量化与模型部署。

### Data
- `processing_2.py`, `processing_class.py`: 数据处理脚本
- `city_db/GeoLite2-City.mmdb`: GeoLite2城市数据库
- `clean_data/data_all.csv`: 清洗后的数据
- `Data-clean/dga-domain.txt`, `top-1m.csv`: 清洗数据
### Model_Deployment
-  `TensorRT.py`:模型部署

### Model_File
- `TransFlexNet.pth`: 保存的模型文件
- `TransFlexNet_PTQ.pth` 量化后的模型文件
### Model_Quantization
-  `PTQ.py`:量化计算
### Train_Model
- `Train_Transformer_R_SKNET.py`: 模型训练脚本
- `log/Transformer+R_SKNET.csv`: 训练过程的日志
- `png/Transformer+R_SKNET.png`: 训练过程生成的图像

## Tools
各种工具脚本，用于支持域名检测服务。

### client_tools
- `get_domain.py`: 用于捕获和处理DNS数据包的异步程序
- `get_loc_ip.py`: 获取系统的网络连接信息

### database_tools
- `dababase_use.py`: 获取当前机器的IP地址信息，并存储到MongoDB数据库

### model_use_tools
- `predict_domain.py`: 用于域名分类预测的模型加载和预测函数

## web_url
提供用户界面的web部分。

### templates/static
- 存放HTML模板和静态文件

### app.py
- 运行Web用户界面的主脚本
### mongo_spark.py
- spark与mongodb联动数据分析任务



## kafka
-   `zkServer.cmd` 启动zkServer
-  `.\bin\windows\kafka-server-start.bat .\config\server.properties`启动kafka
-  `faust -A hello_world worker -l info`启动流处理


