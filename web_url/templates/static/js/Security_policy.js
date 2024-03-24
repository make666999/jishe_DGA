
function updateTime() {
    var now = new Date();
    var hours = String(now.getHours()).padStart(2, '0');
    var minutes = String(now.getMinutes()).padStart(2, '0');
    var seconds = String(now.getSeconds()).padStart(2, '0');
    var currentTimeString = hours + ':' + minutes + ':' + seconds;
    document.querySelector('.current-time').textContent = currentTimeString;
}

// 更新时间并每秒刷新
updateTime();
setInterval(updateTime, 1000);



$('#range').on("input", function() {

    $('.output').val(this.value +"，000条" );
    }).trigger("change");


document.addEventListener('DOMContentLoaded', () => {
   const levels = {
    '安全等级': ['低', '中', '高'],
    '漏洞预警': ['低', '中', '高'],
    '风险指数': ['低', '中', '高'],
    '策略偏向': ['保守', '均衡', '积极']
};

// 初始化每个盒子
document.querySelectorAll('.custom-info-box').forEach(box => {
    const title = box.querySelector('.info-box-title').textContent;
    const content = box.querySelector('.info-box-content');
    const decreaseButton = box.querySelector('.decrease');
    const increaseButton = box.querySelector('.increase');

    decreaseButton.onclick = () => {
        const currentLevelIndex = levels[title].indexOf(content.textContent);
        if (currentLevelIndex > 0) {
            content.textContent = levels[title][currentLevelIndex - 1];
        }
    };

    increaseButton.onclick = () => {
        const currentLevelIndex = levels[title].indexOf(content.textContent);
        if (currentLevelIndex < levels[title].length - 1) {
            content.textContent = levels[title][currentLevelIndex + 1];
        }
    };
});
});


// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('radarChart'));

// 指定图表的配置项和数据
var option = {
    title: {
        text: '雷达扫描效果'
    },
    tooltip: {},
    radar: {
        // shape: 'circle',
        name: {
            textStyle: {
                color: '#fff',
                backgroundColor: '#999',
                borderRadius: 3,
                padding: [3, 5]
           }
        },
        indicator: [
           { name: '销售', max: 6500},
           { name: '管理', max: 16000},
           { name: '信息技术', max: 30000},
           { name: '客户支持', max: 38000},
           { name: '研发', max: 52000},
           { name: '市场', max: 25000}
        ]
    },
    series: [{
        name: '预算 vs 开销',
        type: 'radar',
        data : [
            {
                value : [4300, 10000, 28000, 35000, 50000, 19000],
                name : '预算分配',
                areaStyle: {normal: {}}
            },
             {
                value : [5000, 14000, 28000, 31000, 42000, 21000],
                name : '实际开销',
                areaStyle: {
                    normal: {
                        opacity: 0.9, // 区域透明度
                        shadowBlur: 10, // 阴影模糊大小
                        shadowColor: 'rgba(0, 0, 0, 0.5)' // 阴影颜色
                    }
                }
            }
        ]
    }]
};

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);

// 模拟雷达扫描效果
function radarScan() {
    var index = 0;
    setInterval(function () {
        var data0 = option.series[0].data[0].value;
        var data1 = option.series[0].data[1].value;
        for (var i = 0; i < data0.length; i++) {
            // 随机生成扫描数据
            data0[i] = Math.random() * (option.radar.indicator[i].max - 500) + 500;
            data1[i] = Math.random() * (option.radar.indicator[i].max - 500) + 500;
        }
        myChart.setOption(option);
    }, 2000); // 每两秒更新一次数据
}

radarScan(); // 调用函数，开始扫描

