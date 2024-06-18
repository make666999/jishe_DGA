var ws = new WebSocket(`ws://${serverIp}/Dns_Address_Type`);

ws.onmessage = function(event) {
    updateChart(JSON.parse(event.data));
};

ws.onerror = function() {
    console.log("WebSocket error");
};

ws.onclose = function() {
    console.log("WebSocket connection closed");
};

var myChart = echarts.init(document.getElementById('domain_count3'));

var option = {
    xAxis: {
        type: 'category',
        data: [], // X轴的数据通过WebSocket动态获取
    },
    yAxis: {
        type: 'value',
    },
    series: [{
        type: 'bar',
        data: [], // Y轴的数据通过WebSocket动态获取
    }],
    dataZoom: [{
        type: 'inside' // 启用内置型数据缩放组件
    }]
};

myChart.setOption(option);

myChart.on('click', function (params) {
    const zoomSize = 6;
    const dataAxis = option.xAxis.data; // 确保dataAxis指向当前x轴的数据
    const data = option.series[0].data; // 确保data指向当前系列的数据

    // 计算开始和结束的索引
    const startValue = Math.max(params.dataIndex - Math.floor(zoomSize / 2), 0);
    const endValue = Math.min(params.dataIndex + Math.floor(zoomSize / 2), data.length - 1);

    // 发送数据缩放的动作
    myChart.dispatchAction({
        type: 'dataZoom',
        startValue: startValue,
        endValue: endValue
    });
});
function updateChart(data) {
    let addresses = data.map(item => item.address);  // DNS地址
    let counts = data.map(item => item.count);  // 对应的计数

     let total = counts.reduce((acc, count) => acc + count, 0);
    myChart.setOption({
        xAxis: {
            data: addresses  // 更新x轴数据
        },
        series: [{
            data: counts  // 更新y轴数据
        }]
    });

           document.querySelector('.today_total_count').textContent = total;
}