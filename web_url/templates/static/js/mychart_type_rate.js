var chartContainer = document.getElementById('type_rate');
// chartContainer.style.height = '80%';
// 获取容器的父元素，以便居中
var parentElement = chartContainer.parentElement;

// 实例化图表
var myChart = echarts.init(chartContainer);

// 定义原始高度和宽度
var originalHeight = myChart.getHeight();
var originalWidth = myChart.getWidth();

option = {
    legend: {
        top: 'bottom'
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
            name: 'Nightingale Chart',
            type: 'pie',
            radius: [10, 100],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {
                borderRadius: 8
            },
            data: [
                {value: 38, name: 'bad'},
                {value: 32, name: 'unfind'},
                {value: 30, name: 'BENIGN'},
            ],
            color: ['#FFCC99', '#FFFFCC', '#99CCCC']
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

// 监听窗口大小变化，重新渲染图表并保持在中间位置
window.addEventListener('resize', function () {
    myChart.resize();

    // 重新计算图表容器的位置并居中
    var parentWidth = parentElement.offsetWidth;
    var parentHeight = parentElement.offsetHeight;
    var chartWidth = chartContainer.offsetWidth;
    var chartHeight = chartContainer.offsetHeight;

    chartContainer.style.left = (parentWidth - chartWidth) / 2 + 'px';
    chartContainer.style.top = (parentHeight - chartHeight) / 2 + 'px';
});
