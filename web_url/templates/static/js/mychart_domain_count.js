var chartContainer = document.getElementById('domain_count');

// 实例化图表
var myChart = echarts.init(chartContainer);

// 定义原始高度和宽度
var originalHeight = myChart.getHeight();
var originalWidth = myChart.getWidth();

// 图表的选项
option = {
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
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
                borderRadius: 10
            },
            label: {
                show: false,
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
                {value: 1048, name: 'GOOD'},
                {value: 735, name: 'BAD'},
            ],
            color: ['#99CC99', '#FFCCCC'] // 自定义颜色
        }
    ]
};
// 设置图表选项
myChart.setOption(option);

// 缩小图表一倍
myChart.resize({
    height: originalHeight / 1.2,
    width: originalWidth / 1.2
});

// 监听窗口大小变化，重新渲染图表
window.addEventListener('resize', function () {
    myChart.resize();
});
