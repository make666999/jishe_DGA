document.addEventListener('DOMContentLoaded', function () {
    // 创建图表容器
    var chartContainer = document.getElementById('radar-chart');

    // 初始化图表
    var chart = echarts.init(chartContainer);

    // 图表配置
    var option = {
        title: {
            text: '多模态监控'
        },
        legend: {
            data: ['分布式', '中心化', '混合']
        },
        radar: {
            // shape: 'circle',
            indicator: [
                {name: '架构设计', max: 6500},
                {name: '可扩展性', max: 16000},
                {name: '性能和响应时间', max: 30000},
                {name: '容错性和可靠性', max: 38000},
                {name: '数据安全性', max: 52000},
                {name: '管理和维护成本', max: 25000}
            ]
        },
        series: [
            {
                name: '部署模式多模态比较',
                type: 'radar',
                data: [
                    {
                        value: [4200, 3000, 20000, 35000, 50000, 18000],
                        name: '分布式'
                    },
                    {
                        value: [5000, 14000, 28000, 26000, 42000, 21000],
                        name: '中心化'
                    },
                    {
                        value: [4500, 4000, 4000, 32000, 33000, 20000],
                        name: '混合'
                    }
                ]
            }
        ]
    };

    // 使用配置项显示图表
    chart.setOption(option);

    // 监听窗口大小变化事件，调整图表大小
    window.addEventListener('resize', function () {
        chart.resize();
    });
});
