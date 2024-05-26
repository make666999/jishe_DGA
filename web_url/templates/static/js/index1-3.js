var chartDom = document.getElementById('domain_count3');
var myChart = echarts.init(chartDom);
var option;

// 初始化数据，用于存储每个设备的访问量
const data = [0, 0, 0]; // 初始化为0
option = {
  xAxis: {
    max: 'dataMax'
  },
  yAxis: {
    type: 'category',
    data: [], // 初始化为空数组，后续会更新为设备名称
    inverse: true,
    animationDuration: 300,
    animationDurationUpdate: 300,
    max: 2 // only the largest 3 bars will be displayed
  },
  series: [
    {
      realtimeSort: true,
      name: '不同设备访问量',
      type: 'bar',
      data: data, // 使用上面初始化的数据
      label: {
        show: true,
        position: 'right',
        valueAnimation: true
      }
    }
  ],
  legend: {

  },
  animationDuration: 0,
  animationDurationUpdate: 3000,
  animationEasing: 'linear',
  animationEasingUpdate: 'linear'
};

// 更新图表数据的函数
function updateChartData(data) {
  myChart.setOption({
    yAxis: {
      data: data.map(item => item.collection_name) // 更新纵轴的设备名称
    },
    series: [
      {
        type: 'bar',
        data: data.map(item => item.daily_count) // 更新柱状图的数据
      }
    ]
  });
}

// 初始渲染图表
option && myChart.setOption(option);

// 创建 WebSocket 连接
var ws = new WebSocket(`ws://${serverIp}/websocket_user_list_management`);
ws.onmessage = function (event) {
    var responseData = JSON.parse(event.data);
    updateChartData(responseData.collections_data); // 当收到 WebSocket 消息时更新图表数据
}
