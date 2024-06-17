var currentMap = 'world'; // 初始化当前地图状态为世界地图

$(function () {
    map();

    function map() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('map'));

        // 初始数据
        var data = [
            {name: '海门', value: 9},

        ];

        var geoCoordMap = {
            '海门': [121.15, 31.89],

        };

        var convertData = function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var geoCoord = geoCoordMap[data[i].name];
                if (geoCoord) {
                    res.push({
                        name: data[i].name,
                        value: geoCoord.concat(data[i].value)
                    });
                }
            }
            return res;
        };

        option = {
   // backgroundColor: '#404a59',
title: {
    text: '恶意域名IP定位分析',
    subtext: '来源：360安全实验室',
    sublink: 'https://gitee.com/iGaoWei/big-data-view',
    left: 'right', // 将标题靠右
    textStyle: {
        color: '#fff'
    }
},

    tooltip: {
        trigger: 'item',
        formatter: function (params) {
            return params.name + ' : ' + params.value[2];
        },

    },
    geo: {
        map: 'china',
        label: {
            emphasis: {
                show: false
            }
        },
        roam: false,
		zoom:1.2,
        itemStyle: {
            normal: {
                areaColor: 'rgba(2,37,101,.5)',
                borderColor: 'rgba(112,187,252,.5)'
            },
            emphasis: {
                areaColor: 'rgba(2,37,101,.8)'
            }
        }
    },
    series : [
        {
            name: '标题名称',
            type: 'scatter',
            coordinateSystem: 'geo',
            data: convertData(data),
            symbolSize: function (val) {
                return val[2] / 1000;
            },
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#ffeb7b'
                }
            }
        }

    ]
};

        myChart.setOption(option);

        // 监听地图点击事件
        myChart.on('click', function (params) {
            // 检查点击的是否是地图元素
            if (params.componentType === 'geo') {
                if (currentMap === 'world') {
                    // 从世界地图点击到一个国家的地图
                    myChart.setOption({
                        geo: { map: "china" }, // 切换到对应国家地图
                        series: [
        {
            symbolSize: function (val) {
                    return val[2] / 1000; // 中国地图时的大小调整
            },
            // 其他系列配置
        }
    ]
                    });
                    currentMap = params.name.toLowerCase(); // 更新当前地图状态为该国家
                } else {
                    // 从国家地图点击返回世界地图
                    myChart.setOption({
                        geo: { map: 'world' }, // 切换回世界地图
                        series: [
        {
            symbolSize: function (val) {
                    return val[2] / 1500;
            },
            // 其他系列配置
        }
    ]
                    });
                    currentMap = 'world'; // 更新当前地图状态为世界地图
                }
            }
        });

        window.addEventListener("resize", function () {
            myChart.resize();
        });

        // WebSocket连接
        var ws = new WebSocket(`ws://${serverIp}/Count_Map_Data`);
        ws.onmessage = function (event) {
            var data = JSON.parse(event.data);
            myChart.setOption({
                series: [{
                    data: data
                }]
            });
        };
    }
});
