$(function () {

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

    function totalSales() {
        if ($('#total-sales').length) {
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

            new ApexCharts(document.querySelector("#total-sales"), options).render();
        }
    }

    totalSales();

    function totalOrders() {
        if ($('#total-orders').length) {
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

            new ApexCharts(document.querySelector("#total-orders"), options).render();
        }
    }

    totalOrders();

    function customerRating() {
        if ($('#customer-rating').length) {
            const options = {
                series: [{
                    name: 'Rate',
                    data: [25, 66, 41, 89, 63, 25, 44, 12, 36]
                }],
                chart: {
                    type: 'line',
                    height: 50,
                    sparkline: {
                        enabled: true
                    }
                },
                stroke: {
                    width: 4,
                    curve: 'smooth',
                },
                theme: {
                    mode: $('body').hasClass('dark') ? 'dark' : 'light',
                },
                colors: [colors.success],
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
                                return seriesName;
                            }
                        }
                    },
                    marker: {
                        show: false
                    }
                }
            };

            new ApexCharts(document.querySelector("#customer-rating"), options).render();
        }
    }

    customerRating();

  function salesChart() {
    var ws = new WebSocket("ws://192.168.78.98:8000/collection_stats"); // 更改为你的WebSocket URL
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

    ws.onmessage = function(event) {
        var data = JSON.parse(event.data);
        updateChart(data);


    };

    function updateChart(data) {
    var newSeries = [];
    var categories = Object.keys(data[Object.keys(data)[0]]).sort(); // 假设所有设备都有相同的时间标签

    Object.keys(data).slice(0, 5).forEach(function(device) { // 最多处理五个设备
        var dataPoints = [];
        categories.forEach(function(time) {
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
    var ws = new WebSocket("ws://192.168.78.98:8000/week_day_data_total"); // 更改为你的WebSocket URL

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
                return  val;
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
                    return  val;
                }
            }
        },
        grid: {
            show: false
        }
    };

    chart = new ApexCharts(document.querySelector('#products-sold'), options);
    chart.render();

    ws.onmessage = function(event) {
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
