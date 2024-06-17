$(function () {
    top_dns();
    day_dns();
    map();
    head();
    salesChart();
    device_count();
     function top_dns (){

// 统计用户集合中good和bad的数量
    var chartContainer = document.getElementById('domain_count');

// 实例化图表
    var index_1 = echarts.init(chartContainer);

// 定义原始高度和宽度
    var originalHeight = index_1.getHeight();
    var originalWidth = index_1.getWidth();

// 图表的选项
    var option = {
        legend: {
            top: 'bottom'
        },
        tooltip: {
            trigger: 'item'
        },
        toolbox: {
            show: true,
            right: 10, // 调整水平偏移量
            top: 10, // 调整垂直偏移量
            feature: {}
        },
        series: [
            {
                name: 'Domain Type',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                padAngle: 5,
                itemStyle: {
                    borderRadius: 10
                },
                label: {
                    show: true,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 40,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    {value: 5, name: 'repend'}, // 初始值设为0
                    {value: 1, name: 'attact'}, // 初始值设为0
                ],
                color: ['#99CC99', '#FFCCCC'] // 自定义颜色
            }
        ]
    };

// 设置图表选项
    index_1.setOption(option);

// 缩小图表一倍
    index_1.resize({
        height: originalHeight / 1.2,
        width: originalWidth / 1.2
    });

// 监听窗口大小变化，重新渲染图表
    window.addEventListener('resize', function () {
        index_1.resize();
    });

// 创建WebSocket连接
    var ws = new WebSocket(`ws://${serverIp}/websocket_dns_traffic_security_analysis`);

    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var totalBenign = 0;
        var totalNonBenign = 0;
        data.stats.forEach(function (stat) {
            totalBenign += stat.benign_count;
            totalNonBenign += stat.non_benign_count;
        });
        document.querySelector('.data_counts').textContent = data.day_counts;

        // 更新图表数据
        index_1.setOption({
            series: [{
                data: [
                    {value: totalBenign, name: 'repend'},
                    {value: totalNonBenign, name: 'attact'}
                ]
            }]
        });
    };

};
     function day_dns() {
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


     };
     function map() {
         var myChart2 = echarts.init(document.getElementById('map'));
    myChart2.showLoading();

    // Initial configuration for the ECharts instance
    myChart2.setOption({

        geo3D: {
            map: 'world',
            shading: 'realistic',
            silent: true,
            environment: '#333',
            realisticMaterial: {
                roughness: 0.8,
                metalness: 0
            },
            postEffect: {
                enable: true
            },
            groundPlane: {
                show: false
            },
            light: {
                main: {
                    intensity: 1,
                    alpha: 30
                },
                ambient: {
                    intensity: 0
                }
            },
            viewControl: {
                distance: 70,
                alpha: 89,
                panMouseButton: 'left',
                rotateMouseButton: 'right'
            },
            itemStyle: {
                color: '#000'
            },
            regionHeight: 0.5
        },
        series: [{
            type: 'lines3D',
            coordinateSystem: 'geo3D',
            effect: {
                show: true,
                trailWidth: 1.5, // 增加尾迹宽度
                trailOpacity: 0.8, // 增加尾迹透明度
                trailLength: 0.5, // 增加尾迹长度
                constantSpeed: 8
            },
            blendMode: 'lighter',
            lineStyle: {
                width: 0.2,
                opacity: 0.05
            },
            data: [] // Initially empty data
        }]
    });

    // Hide loading after the initial setup
    myChart2.hideLoading();

    // Setup WebSocket connection
    var ws = new WebSocket(`ws://${serverIp}/city_map`);
    ws.onmessage = function (event) {
        var routes = JSON.parse(event.data); // Parse the JSON data received from the server
        console.log(routes); // Log data for debugging

        // Update the chart with new routes data
        myChart2.setOption({
            series: [{
                data: routes // Set the received routes as data for the series
            }]
        });
    };

    // Toggle effects on keydown
    window.addEventListener('keydown', function () {
        myChart2.dispatchAction({
            type: 'lines3DToggleEffect',
            seriesIndex: 0
        });
    });

     }
     function head() {
         var ws = new WebSocket(`ws://${serverIp}/websocket_daily_top_remain_type`);
    ws.onmessage = function (event) {
        // 解析从服务器接收到的数据
        var data = JSON.parse(event.data);
        var topTypesDaily = data.top_types_daily;
        document.querySelector('.today_total_count').textContent = data.today_total_count;
     }}
    function device_count() {
          var ws = new WebSocket(`ws://${serverIp}/websocket_get_data_formatted`);
    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var deviceList = document.getElementById('device-list');
        var deviceCount = document.getElementById('device-count'); // 获取显示设备数量的元素

        deviceList.innerHTML = ''; // 清空现有的列表项
        deviceCount.textContent = data.total_collections; // 更新设备数量
        document.querySelector('.on_online').textContent = data.on_online;

        // 遍历每个集合的数据
        data.collections_data.forEach(function (collection) {
            // 创建新的列表项
            var listItem = document.createElement('div');
            listItem.className = 'list-group-item d-flex justify-content-between align-items-center px-0';

            // 设置集合名称和Loc_Address数据
            listItem.innerHTML = `
            <div class="d-flex flex-grow-1 align-items-center">
                <img width="30" style=" margin-right: 0.5rem !important" src="static/picture/computer.png" > <!-- 更换为适当的图标或去除 -->
                <span>${collection.collection_name}</span>
            </div>
            <span>${collection.latest_loc_address}</span>
        `;

            // 将新的列表项添加到设备列表中
            deviceList.appendChild(listItem);
        });
    };


    }
    function salesChart() {
        var ws = new WebSocket(`ws://${serverIp}/websocket_poll_cluster_statistics`);

        var chart; // 在函数外部声明图表变量

        // 初始化图表
        const options = {
            series: [],
            chart: {
                height: 350,
                type: 'line',
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                width: 4,
                curve: 'smooth'
            },
            xaxis: {
                categories: [],
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val + " units";
                    }
                }
            },
            legend: {
                show: true
            }
        };
        chart = new ApexCharts(document.querySelector("#sales-chart"), options);
        chart.render();

        ws.onmessage = function (event) {
            var data = JSON.parse(event.data);
            updateChart(data);
        };

        function updateChart(data) {
            var newSeries = [];
            var categories = Object.keys(data[Object.keys(data)[0]]).sort(); // 假设所有设备都有相同的时间标签

            Object.keys(data).slice(0, 5).forEach(function (device) { // 最多处理五个设备
                var dataPoints = [];
                categories.forEach(function (time) {
                    dataPoints.push(data[device][time]);
                });
                newSeries.push({
                    name: device,
                    data: dataPoints
                });
            });

            // 仅更新图表的数据系列，而不是整个图表
            chart.updateSeries(newSeries);

            // 仅在必要时更新分类轴（x轴）
            chart.updateOptions({
                xaxis: {
                    categories: categories
                }
            }, true, false); // 第二个参数表示是否重绘动画，第三个参数表示是否更新所有配置项
        }

    }


     })
