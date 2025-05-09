$(function () {
    now_data();
    top_dns();
    day_dns();
    map();

    salesChart();
    device_count();
    acc();

    //表头数据
    function now_data() {
        var ws = new WebSocket(`ws://${serverIp}/lisen`);
        ws.onmessage = function (event) {
            // 解析从服务器接收到的数据
            var data = JSON.parse(event.data);
            // console.log(data);
            document.querySelector('.data_counts').textContent = data.all_count; //集群域名访问量
            document.querySelector('.dga_now').textContent = data.dga_count; //集群域名访问量
            document.querySelector('.today_total_count').textContent = data.remote_domain_count;

            // console.log("ok");
        }
    };

    //恶意域名统计
    function top_dns() {

        // 获取图表容器并设置样式
        var chartContainer = document.getElementById('domain_count');
        chartContainer.style.width = '100%';
        chartContainer.style.height = '100%';

        // 实例化图表
        var index_1 = echarts.init(chartContainer);

        // 图表的选项
        var option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                top: 'bottom',
                data: ['repend', 'attact']
            },
            toolbox: {
                show: true,
                right: 10,
                top: 10,
                feature: {}
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: [] // 初始化为空，稍后填充
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: 'repend',
                    type: 'line',
                    smooth: true,
                    data: [], // 初始化为空，稍后填充
                    lineStyle: {
                        width: 3
                    },
                    itemStyle: {
                        color: '#99CC99'
                    }
                },
                {
                    name: 'attact',
                    type: 'line',
                    smooth: true,
                    data: [], // 初始化为空，稍后填充
                    lineStyle: {
                        width: 3
                    },
                    itemStyle: {
                        color: '#FFCCCC'
                    }
                }
            ]
        };

        // 设置图表选项
        index_1.setOption(option);

        // 监听窗口大小变化，重新渲染图表
        window.addEventListener('resize', function () {
            index_1.resize();
        });

        // 创建WebSocket连接
        var ws = new WebSocket(`ws://${serverIp}/lisen_all`);

        let latestData = null; // 保存最近一次的 payload 数据

        ws.onmessage = function (event) {
            latestData = JSON.parse(event.data); // 缓存数据，不立即渲染
        };

        setInterval(function () {
            if (!latestData) return;

            var totalBenign = [];
            var totalNonBenign = [];
            var dates = [];

            latestData.stats.forEach(function (stat) {
                dates.push(stat.collection_name);
                totalBenign.push(stat.benign_count);
                totalNonBenign.push(stat.non_benign_count);
            });

            index_1.setOption({
                xAxis: {
                    data: dates
                },
                series: [
                    {
                        name: 'repend',
                        data: totalBenign
                    },
                    {
                        name: 'attact',
                        data: totalNonBenign
                    }
                ]
            });

        }, 3000); // 每 3 秒触发一次

    };

    //集群设备数据访问量
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
            legend: {},
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
                        data: data.map(item => item.benign_count + item.non_benign_count) // 更新柱状图的数据
                    }
                ]
            });
        }

// 初始渲染图表
        option && myChart.setOption(option);
        let latestData = null; // 用于缓存最近一次 WebSocket 收到的数据
// 创建 WebSocket 连接
        var ws = new WebSocket(`ws://${serverIp}/lisen_all`);
        ws.onmessage = function (event) {
            var responseData = JSON.parse(event.data);
            latestData = responseData.stats; // 缓存 stats 数据
        };
        setInterval(function () {
            if (!latestData) return;

            updateChartData(latestData);
        }, 2000);

    };

    //地图数据
    function map() {
        var myChart2 = echarts.init(document.getElementById('map'));
        myChart2.showLoading();

        // Initial configuration for the ECharts instance
        myChart2.setOption({

            geo3D: {
                map: 'world',
                shading: 'realistic',
                silent: true,
                environment: '#ffffff',
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
                    color: 'rgba(142,226,245,0.75)'
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
                lineStyle: {
                    width: 0.2,
                    opacity: 0.05,
                    color: 'rgba(19,107,69,0.83)' // 设置飞线颜色为红色
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
            // console.log(routes); // Log data for debugging

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

    };


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

    //十分钟数据统计
    function salesChart() {
        var ws = new WebSocket(`ws://${serverIp}/lisen_now_10min`);
        var chart = echarts.init(document.getElementById('sales-chart'));

        var latestData = null;  // 用于缓存最新数据

        var option = {
            grid: {
                left: '3%',
                right: '4%',
                bottom: '8%',
                top: '15%',
                containLabel: true
            },
            tooltip: {trigger: 'axis'},
            legend: {
                top: '5%',
                data: []
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                axisLabel: {
                    rotate: 0
                },
                data: []
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value} units'
                }
            },
            series: []
        };

        chart.setOption(option);

        // 接收数据后缓存
        ws.onmessage = function (event) {
            latestData = JSON.parse(event.data);
        };

        // 每2秒刷新一次图表
        setInterval(function () {
            if (latestData) {
                updateChart(latestData);
            }
        }, 2000);

        function updateChart(data) {
            var categories = data.ts;
            var legendData = Object.keys(data.counts);
            var series = [];

            legendData.forEach(function (device) {
                series.push({
                    name: device,
                    type: 'line',
                    smooth: true,
                    data: data.counts[device]
                });
            });

            chart.setOption({
                legend: {data: legendData},
                xAxis: {data: categories},
                series: series
            });
        }
    }


    function acc() {
        var myChart = echarts.init(document.getElementById('echart4'));
        var socket = new WebSocket(`ws://${serverIp}/websocket_top_five_messages`);

        socket.onmessage = function (event) {
            var rawData = JSON.parse(event.data);
            // 处理接收到的数据以适应 echarts 图表
            var xAxisData = [];
            var yAxisData = [];
            rawData.forEach(function (item) {
                xAxisData.push(item.toName);  // 将地名添加到x轴
                yAxisData.push(item.count);   // 将对应计数添加到y轴
            });

            var option = {
                color: ["#FF4500", "#1E90FF", "#32CD32", "#FFD700", "#FF69B4"],
                grid: {
                    left: "3%",
                    right: "4%",
                    bottom: "3%",
                    containLabel: true
                },
                xAxis: [{
                    type: "category",
                    data: xAxisData,  // 使用处理后的x轴数据
                    boundaryGap: true,
                    axisLine: {
                        show: true,
                    },
                    axisLabel: {
                        interval: 0,
                        margin: 16,
                        color: "#666666",
                        fontSize: 12,
                    },
                    axisTick: {
                        show: false,
                    },
                }],
                yAxis: [{
                    type: "value",
                    show: false,
                }],
                series: [{
                    name: "地区",
                    type: "bar",
                    barWidth: "50%",
                    data: yAxisData.map(value => ({
                        value: value,
                        label: {
                            show: true,
                            position: "top",
                            color: "#FF6900",
                            formatter({value}) {
                                return `${value}条`;
                            },
                        },
                        itemStyle: {
                            color: "#FF6900",
                            borderWidth: 2,
                            borderType: "solid",
                            borderColor: "#FF6900",
                        }
                    })),
                    avoidLabelOverlap: false,
                    hoverAnimation: false,

                    // 统一设置其他的 未单独设置样式的 数据柱状图样式
                    itemStyle: {
                        borderRadius: [50, 50, 0, 0],
                        borderWidth: 2,
                        borderType: "solid",
                        borderColor: "#4D94F1",
                    },
                    label: {
                        show: true,
                        position: "top",
                        color: "#4D94F1",
                        formatter({value}) {
                            return `${value}条`;
                        },
                    },

                    labelLine: {
                        show: false,
                    },
                }]
            };

            myChart.setOption(option);
        };

        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }


})
