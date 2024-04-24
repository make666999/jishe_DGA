系统介绍：本作品的DGA集成式风控感知管理服务系统通过定制化安全策略、大数据分析及多策略轻量化部署，提高了网络安全防御的效果和灵活性。
高效的DNS流量监控与响应：
利用高性能的异步技术，系统能够持续且高效地监视网络流量。
配备有应急响应功能，按照定制化的安全策略实时减少安全风险。
集群安全状态分析：
结合了大数据技术，进行深入的DNS流量数据分析。
提供全面的集群威胁视角和状态感知，支持数据驱动的决策过程。
集群设备监控管理：
支持集群中单个设备的详尽管理和监控。
包括服务与安全状态管理、DNS流量监控和设备信息维护。
多策略轻量化部署：
支持不同策略的灵活部署，以适应多样化的性能和资源要求。
确保系统的灵活性和可扩展性。
安全策略定制：
允许用户根据业务和安全需求灵活调整防御机制。
确保风险管理符合严格的安全标准。


系统整体文件结构如下
├─.idea
├─Model
│  ├─Data
│  ├─Model_File
│  │      Transformer+R_SKNET.pth
│  └─Train_Model
├─Tools
│  ├─client_tools
│  ├─database_tools
│  └─model_use_tools
│
└─web_url
    │  app.py
    │
    ├─templates
    │  ├─ index.html
    │  ├─files
    │  └─static
    │      ├─css
    │      ├─ditu
    │      ├─font
    │      ├─image
    │      ├─js
    │      └─picture
    └─main.py

Model目录：包含自适应感知模型文件和训练模型。
Tools目录：存储客户端工具、数据库工具和模型使用工具。
web_url目录：包含UI设计文件，系统运行时首先运行web_url下的app.py。
templates目录：存放前端模板文件，如index.html。
static目录：包括CSS样式表、地图、字体、图片、JavaScript脚本和其他媒体文件。
main.py：用于获取本机与互联网间的通信，运行系统时应保持其在运行状态。
