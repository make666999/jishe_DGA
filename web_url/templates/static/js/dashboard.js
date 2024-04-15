//地图显示
var uploadedDataURL = "flight.json";
var myChart2 = echarts.init(document.getElementById('main'));

myChart2.showLoading();
$.getJSON(uploadedDataURL, function (data) {
    myChart2.hideLoading();

    function getAirportCoord(idx) {
        return [data.airports[idx][3], data.airports[idx][4]];
    }

    var routes = data.routes.map(function (airline) {
        return [getAirportCoord(airline[1]), getAirportCoord(airline[2])];
    });

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
        series: [
            {
                type: 'lines3D',
                coordinateSystem: 'geo3D',
                effect: {
                    show: true,
                    trailWidth: 1,
                    trailOpacity: 0.5,
                    trailLength: 0.2,
                    constantSpeed: 5
                },
                blendMode: 'lighter',
                lineStyle: {
                    width: 0.2,
                    opacity: 0.05
                },
                data: routes
            }
        ]
    });
    window.addEventListener('keydown', function () {
        myChart2.dispatchAction({
            type: 'lines3DToggleEffect',
            seriesIndex: 0
        });
    });
});

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


    function salesChart() {
        var ws = new WebSocket(`ws://${serverIp}/collection_stats`);


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
            }, false, false); // 第二个参数表示是否重绘动画，第三个参数表示是否更新所有配置项
        }

    }

    salesChart();


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
        var ws = new WebSocket(`ws://${serverIp}/week_day_data_total`);


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

            // 假设数据格式为 { '2024-03-10': 10, '2024-03-11': 15, ... }
            for (const [date, count] of Object.entries(data)) {
                // 转换日期格式从 'YYYY-MM-DD' 到 'MM-DD'
                const shortDate = date.substring(5); // 移除前4个字符和分隔符
                categories.push(shortDate);
                originalDataSeries.push({date: shortDate, count: count});
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
        }


    }

    productsSold(); // 调用函数以初始化图表和WebSocket连接


// 更新数据列表
    // 建立WebSocket连接

    var ws = new WebSocket(`ws://${serverIp}/latest_location_data`);
    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var deviceList = document.getElementById('device-list');
        var deviceCount = document.getElementById('device-count'); // 获取显示设备数量的元素

        deviceList.innerHTML = ''; // 清空现有的列表项
        deviceCount.textContent = data.total_collections; // 更新设备数量

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

// 统计用户集合中good和bad的数量
    var chartContainer = document.getElementById('domain_count');

// 实例化图表
    var myChart = echarts.init(chartContainer);

// 定义原始高度和宽度
    var originalHeight = myChart.getHeight();
    var originalWidth = myChart.getWidth();

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
                    {value: 0, name: 'repend'}, // 初始值设为0
                    {value: 0, name: 'attact'}, // 初始值设为0
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

// 创建WebSocket连接
    var ws = new WebSocket(`ws://${serverIp}/count_benign_nonbenign`);

    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var totalBenign = 0;
        var totalNonBenign = 0;
        data.stats.forEach(function (stat) {
            totalBenign += stat.benign_count;
            totalNonBenign += stat.non_benign_count;
        });
        // 更新图表数据
        myChart.setOption({
            series: [{
                data: [
                    {value: totalBenign, name: 'BENIGN'},
                    {value: totalNonBenign, name: 'NON-BENIGN'}
                ]
            }]
        });
    };


// 第一个框，第二个图表
    // 统计用户集合中good和bad的数量
    var chartContainer = document.getElementById('domain_count2');

// 实例化图表
    var myChart = echarts.init(chartContainer);

// 定义原始高度和宽度
    var originalHeight = myChart.getHeight();
    var originalWidth = myChart.getWidth();

// 图表的选项
    option = {
        angleAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        radiusAxis: {},
        polar: {},
        series: [
            {
                type: 'bar',
                data: [1, 2, 3, 4, 3, 5, 1],
                coordinateSystem: 'polar',
                name: 'A',
                stack: 'a',
                emphasis: {
                    focus: 'series'
                }
            },
            {
                type: 'bar',
                data: [2, 4, 6, 1, 3, 2, 1],
                coordinateSystem: 'polar',
                name: 'B',
                stack: 'a',
                emphasis: {
                    focus: 'series'
                }
            },
            {
                type: 'bar',
                data: [1, 2, 3, 4, 1, 2, 5],
                coordinateSystem: 'polar',
                name: 'C',
                stack: 'a',
                emphasis: {
                    focus: 'series'
                }
            }
        ],

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


// 第一个框的第三个图


//统计五天域名访问量最高的数据
    var chartContainer = document.getElementById('domain_kinds');
    var myChart = echarts.init(chartContainer);

// 初始化空数据
    var dates = [];
    var values = [];
    var topTypes = [];

// WebSocket连接
    var ws = new WebSocket(`ws://${serverIp}/top_remain_type_daily`);


    ws.onmessage = function (event) {
        // 解析从服务器接收到的数据
        var data = JSON.parse(event.data);
        var topTypesDaily = data.top_types_daily;

        // 清空当前数据
        dates = [];
        values = [];
        topTypes = [];

        // 填充新数据
        topTypesDaily.forEach(function (item) {
            dates.push(item.date);
            values.push(item.count);
            topTypes.push({
                value: item.count,

                symbolSize: 50 // 可以根据需要调整大小
            });
        });

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
                    // 使用默认形状为所有条目
                    data: topTypes.map(item => ({...item, symbol: 'circle'})) // 这里假设所有条目都使用圆形图标
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


// 监听窗口大小变化，重新渲染图表
    window.addEventListener('resize', function () {
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

