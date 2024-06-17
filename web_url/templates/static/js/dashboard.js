
$(function () {

    var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var wsHost = window.location.hostname;
    // Dashboard chart colors
    const body_styles = window.getComputedStyle(document.body);
    const colors = {
        primary: $.trim(body_styles.getPropertyValue('--bs-primary')),
        secondary: $.trim(body_styles.getPropertyValue('--bs-secondary')),
        info: $.trim(body_styles.getPropertyValue('--bs-info')),
        success: $.trim(body_styles.getPropertyValue('--bs-success')),
        danger: $.trim(body_styles.getPropertyValue('--bs-danger')),
        warning: $.trim(body_styles.getPropertyValue('--bs-warning')),
        light: $.trim(body_styles.getPropertyValue('--bs-light')),
        dark: $.trim(body_styles.getPropertyValue('--bs-dark')),
        blue: $.trim(body_styles.getPropertyValue('--bs-blue')),
        indigo: $.trim(body_styles.getPropertyValue('--bs-indigo')),
        purple: $.trim(body_styles.getPropertyValue('--bs-purple')),
        pink: $.trim(body_styles.getPropertyValue('--bs-pink')),
        red: $.trim(body_styles.getPropertyValue('--bs-red')),
        orange: $.trim(body_styles.getPropertyValue('--bs-orange')),
        yellow: $.trim(body_styles.getPropertyValue('--bs-yellow')),
        green: $.trim(body_styles.getPropertyValue('--bs-green')),
        teal: $.trim(body_styles.getPropertyValue('--bs-teal')),
        cyan: $.trim(body_styles.getPropertyValue('--bs-cyan')),
        chartTextColor: $('body').hasClass('dark') ? '#6c6c6c' : '#b8b8b8',
        chartBorderColor: $('body').hasClass('dark') ? '#444444' : '#ededed',
    };

    $(document).on('click', '.select-all', function () {
        const that = $(this),
            target = $(that.data('select-all-target')),
            checkbox = target.find('input[type="checkbox"]');

        if (that.prop('checked')) {
            checkbox.closest('tr').addClass('tr-selected');
            checkbox.prop('checked', true);
        } else {
            checkbox.closest('tr').removeClass('tr-selected');
            checkbox.prop('checked', false);
        }
    });

    $(document).on('click', '#recent-products input[type="checkbox"]', function () {
        const that = $(this);

        if (that.prop('checked')) {
            that.closest('tr').addClass('tr-selected');
        } else {
            that.closest('tr').removeClass('tr-selected');
        }
    });

    function total1() {
        if ($('#total-1').length) {
            const options = {
                series: [{
                    data: [25, 66, 41, 89, 63, 30, 50]
                }],
                chart: {
                    type: 'line',
                    width: 100,
                    height: 35,
                    sparkline: {
                        enabled: true
                    }
                },
                theme: {
                    mode: $('body').hasClass('dark') ? 'dark' : 'light',
                },
                colors: [colors.indigo],
                stroke: {
                    width: 4,
                    curve: 'smooth',
                },
                tooltip: {
                    fixed: {
                        enabled: false
                    },
                    x: {
                        show: false
                    },
                    y: {
                        title: {
                            formatter: function (seriesName) {
                                return ''
                            }
                        }
                    },
                    marker: {
                        show: false
                    }
                }
            };

            new ApexCharts(document.querySelector("#total-1"), options).render();
        }
    }

    total1();

    function total2() {
        if ($('#total-2').length) {
            const options = {
                series: [{
                    data: [35, 46, 22, 56, 43, 39, 40]
                }],
                chart: {
                    type: 'line',
                    width: 100,
                    height: 35,
                    sparkline: {
                        enabled: true
                    }
                },
                theme: {
                    mode: $('body').hasClass('dark') ? 'dark' : 'light',
                },
                colors: [colors.pink],
                stroke: {
                    width: 4,
                    curve: 'smooth',
                },
                tooltip: {
                    fixed: {
                        enabled: false
                    },
                    x: {
                        show: false
                    },
                    y: {
                        title: {
                            formatter: function (seriesName) {
                                return ''
                            }
                        }
                    },
                    marker: {
                        show: false
                    }
                }
            };

            new ApexCharts(document.querySelector("#total-2"), options).render();
        }
    }

    total2();

    function total3() {
        if ($('#total-3').length) {
            const options = {
                series: [{
                    data: [55, 23, 78, 16, 60, 39, 54]
                }],
                chart: {
                    type: 'line',
                    width: 100,
                    height: 35,
                    sparkline: {
                        enabled: true
                    }
                },
                theme: {
                    mode: $('body').hasClass('dark') ? 'dark' : 'light',
                },
                colors: [colors.blue],
                stroke: {
                    width: 4,
                    curve: 'smooth',
                },
                tooltip: {
                    fixed: {
                        enabled: false
                    },
                    x: {
                        show: false
                    },
                    y: {
                        title: {
                            formatter: function (seriesName) {
                                return ''
                            }
                        }
                    },
                    marker: {
                        show: false
                    }
                }
            };

            new ApexCharts(document.querySelector("#total-3"), options).render();
        }
    }

    total3();

        function total4() {
        if ($('#total-4').length) {
            const options = {
                series: [{
                    data: [59, 35, 47, 38, 45, 21, 56]
                }],
                chart: {
                    type: 'line',
                    width: 100,
                    height: 35,
                    sparkline: {
                        enabled: true
                    }
                },
                theme: {
                    mode: $('body').hasClass('dark') ? 'dark' : 'light',
                },
                colors: [colors.green],
                stroke: {
                    width: 4,
                    curve: 'smooth',
                },
                tooltip: {
                    fixed: {
                        enabled: false
                    },
                    x: {
                        show: false
                    },
                    y: {
                        title: {
                            formatter: function (seriesName) {
                                return ''
                            }
                        }
                    },
                    marker: {
                        show: false
                    }
                }
            };

            new ApexCharts(document.querySelector("#total-4"), options).render();
        }
    }

    total4();

    function initializeCustomerRatings() {
        // 为左侧图表定义选项
        const optionsLeft = {
            series: [{
                name: 'Left Rate',
                data: [25, 66, 41, 90, 12]  // 示例数据
            }],
            chart: {
                type: 'line',
                height: 40,
                sparkline: {
                    enabled: true
                }
            },
            stroke: {
                width: 3,
                curve: 'smooth',
            },
            theme: {
                mode: $('body').hasClass('dark') ? 'dark' : 'light',
            },
            colors: ['rgb(58,163,171)'],  // 自定义颜色
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar'] // 简化的X轴标签
            },
            tooltip: {
                enabled: false
            }
        };

        // 为右侧图表定义选项
        const optionsRight = {
            series: [{
                name: 'Right Rate',
                data: [89, 63, 25, 34, 23]  // 示例数据
            }],
            chart: {
                type: 'line',
                height: 40,
                sparkline: {
                    enabled: true
                }
            },
            stroke: {
                width: 3,
                curve: 'smooth',
            },
            theme: {
                mode: $('body').hasClass('dark') ? 'dark' : 'light',
            },
            colors: ['rgb(13,36,94)'],  // 自定义颜色
            xaxis: {
                categories: ['Apr', 'May', 'Jun'] // 简化的X轴标签
            },
            tooltip: {
                enabled: false
            }
        };

        // 初始化左侧图表
        if ($('#customer-rating-left').length) {
            new ApexCharts(document.querySelector("#customer-rating-left"), optionsLeft).render();
        }
        // 初始化右侧图表
        if ($('#customer-rating-right').length) {
            new ApexCharts(document.querySelector("#customer-rating-right"), optionsRight).render();
        }
    }

    $(document).ready(function () {
        initializeCustomerRatings();
    });





    function salesChannels() {
        if ($('#sales-channels').length) {
            const options = {
                chart: {
                    height: 250,
                    type: 'donut',
                    offsetY: 0
                },
                plotOptions: {
                    pie: {
                        donut: {
                            size: '40%',
                        }
                    }
                },
                stroke: {
                    show: false,
                    width: 0
                },
                colors: [colors.orange, colors.cyan, colors.indigo],
                series: [48, 30, 22],
                labels: ['Social Media', 'Google', 'Email'],
                legend: {
                    show: false
                }
            }

            new ApexCharts(document.querySelector('#sales-channels'), options).render();
        }
    }

    salesChannels();


    function productsSold() {
        var ws = new WebSocket(`ws://${serverIp}/week_day_count`);

        // 初始化图表
        const options = {
            series: [{
                name: 'Total',
                data: []
            }],
            chart: {
                type: 'bar',
                height: 180,
                foreColor: 'rgba(255,255,255,55%)',
                toolbar: {
                    show: false
                }
            },
            theme: {
                mode: $('body').hasClass('dark') ? 'dark' : 'light',
            },
            plotOptions: {
                bar: {
                    borderRadius: 6,
                    columnWidth: '35%',
                }
            },
            colors: ['rgba(255,255,255,60%)'],
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val;
                },
                offsetY: -20,
                style: {
                    fontSize: '12px',
                    colors: ['rgba(255,255,255,55%)']
                }
            },
            xaxis: {
                categories: [],
            },
            yaxis: {
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false,
                },
                labels: {
                    show: false,
                    formatter: function (val) {
                        return val;
                    }
                }
            },
            grid: {
                show: false
            }
        };

        chart = new ApexCharts(document.querySelector('#products-sold'), options);
        chart.render();

        ws.onmessage = function (event) {
            var data = JSON.parse(event.data);
            updateChart(data);
        };

        function updateChart(data) {
            var categories = []; // 用于存储日期
            var originalDataSeries = []; // 用于存储原始的销售数据
             var totalCount = 0; // 用于计算总数

            // 假设数据格式为 { '2024-03-10': 10, '2024-03-11': 15, ... }
            for (const [date, count] of Object.entries(data)) {
                // 转换日期格式从 'YYYY-MM-DD' 到 'MM-DD'
                const shortDate = date.substring(5); // 移除前4个字符和分隔符
                categories.push(shortDate);
                originalDataSeries.push({date: shortDate, count: count});
                 totalCount += count; // 累加总数
            }

            // 对日期和数据进行升序排序
            originalDataSeries.sort((a, b) => {
                // 转换回 'YYYY-MM-DD' 格式进行正确的日期比较
                return new Date(`2020-${a.date}`).getTime() - new Date(`2020-${b.date}`).getTime();
            });

            // 分离排序后的日期和数据
            const sortedCategories = originalDataSeries.map(item => item.date);
            const sortedDataSeries = originalDataSeries.map(item => item.count);

            // 更新图表而不是创建新的
            chart.updateOptions({
                xaxis: {
                    categories: sortedCategories
                },
                series: [{
                    name: 'Total',
                    data: sortedDataSeries
                }]
            });
              document.getElementById('total-1').textContent = totalCount;
        }
    }

    productsSold(); // 调用函数以初始化图表和WebSocket连接


// 更新数据列表
    // 建立WebSocket连接

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
                <img width="45" class="me-3" src="static/picture/computer.png" alt="..."> <!-- 更换为适当的图标或去除 -->
                <span>${collection.collection_name}</span>
            </div>
            <span>${collection.latest_loc_address}</span>
        `;

            // 将新的列表项添加到设备列表中
            deviceList.appendChild(listItem);
        });
    };

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////第一个大框的第一个


// 第一个框，第二个图表

var chartDom = document.getElementById('domain_count2');
var myChart2 = echarts.init(chartDom);

var option = {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    legend: {
        type: 'scroll',
        orient: 'vertical',
        right: 10,
        top: 20,
        bottom: 20
    },
    series: [
        {
            name: '域名类型',
            type: 'pie',
            radius: '55%',
            center: ['40%', '50%'],
            data: [],  // 初始数据为空
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

myChart2.setOption(option);

 var ws = new WebSocket(`ws://192.168.78.98:8000/dga_type_analyze`);

ws.onmessage = function (event) {
    var newData = JSON.parse(event.data);
    updateChart(newData);
};

function updateChart(data) {
    var processedData = processData(data);
    myChart2.setOption({
        series: [{
            data: processedData
        }]
    });
}

function processData(rawData) {
    let aggregatedData = {};

    rawData.forEach(item => {
        if (aggregatedData[item.Domain_Type]) {
            aggregatedData[item.Domain_Type] += item.Count;
        } else {
            aggregatedData[item.Domain_Type] = item.Count;
        }
    });

    return Object.keys(aggregatedData).map(key => ({
        name: key,
        value: aggregatedData[key]
    }));
}


// 第一个框的第三个图


var chartContainer = document.getElementById('domain_kinds');
var myChart = echarts.init(chartContainer);

// 初始化空数据
var dates = [];
var values = [];
var topTypes = [];

// WebSocket连接
var ws = new WebSocket(`ws://${serverIp}/week_day_count_type`);

ws.onmessage = function (event) {
    var data = JSON.parse(event.data);

    // 假设数据结构是 { "2024-06-01": 100, "2024-06-02": 120 }
    dates = Object.keys(data);
    values = Object.values(data);
    topTypes = values.map(value => ({
        value: value,
        symbolSize: 50 // 根据值调整大小
    }));

    // 更新图表
    myChart.setOption({
        xAxis: {
            data: dates
        },
        series: [
            {
                name: 'Top Domain Type Count',
                data: values
            },
            {
                name: 'Top Domain Type',
                data: topTypes
            }
        ]
    });
};

// 图表的初始选项
var option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'none'
        },
        formatter: function (params) {
            return params[0].name + ': ' + params[0].value;
        }
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
    xAxis: {
        data: dates, // 初始日期数据为空
        axisTick: {show: false},
        axisLine: {show: false},
        axisLabel: {
            color: '#e54035'
        }
    },
    yAxis: {
        splitLine: {show: false},
        axisTick: {show: false},
        axisLine: {show: false},
        axisLabel: {show: false}
    },
    color: ['#e54035'],
    series: [
        {
            name: 'Top Domain Type Count',
            type: 'pictorialBar',
            barCategoryGap: '-130%',
            symbol: 'path://M0,10 L10,10 C5.5,10 5.5,5 5,0 C4.5,5 4.5,10 0,10 z',
            itemStyle: {
                opacity: 0.5
            },
            emphasis: {
                itemStyle: {
                    opacity: 1
                }
            },
            data: values, // 初始值数据为空
            z: 10
        },
        {
            name: 'Top Domain Type',
            type: 'pictorialBar',
            barGap: '-100%',
            symbolPosition: 'end',
            symbolSize: 50,
            symbolOffset: [0, '-120%'],
            data: topTypes // 初始类型数据为空
        }
    ]
};

// 设置图表选项
myChart.setOption(option);

// 监听窗口大小变化，调整图表大小
window.addEventListener("resize", function () {
    myChart.resize();
});



    if ($('.summary-cards').length) {
        $('.summary-cards').slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 1500,
            rtl: $('body').hasClass('rtl') ? true : false
        });
    }

});

// 基于准备好的dom，初始化echarts实例

