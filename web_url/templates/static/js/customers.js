$(function () {

    // Dashboard chart colors
    let body_styles = window.getComputedStyle(document.body);
    let colors = {
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

   function newCustomers() {
    // 初始化图表配置
    let options = {
        series: [
            {
                name: 'Customers',
                data: []  // 初始为空，稍后填充
            }
        ],
        chart: {
            height: 280,
            type: 'line',
            offsetX: -15,
            width: '103%',
            foreColor: colors.chartTextColor,
            zoom: {
                enabled: false
            },
            toolbar: {
                show: false
            }
        },
        dataLabels: {
            enabled: false
        },
        theme: {
            mode: $('body').hasClass('dark') ? 'dark' : 'light',
        },
        colors: [colors.primary],
        stroke: {
            width: 4,
            curve: 'smooth'
        },
        legend: {
            show: false
        },
        markers: {
            size: 0,
            hover: {
                sizeOffset: 6
            }
        },
        xaxis: {
            categories: [],  // 初始为空，稍后填充
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val;
                }
            }
        },
        grid: {
            borderColor: colors.chartBorderColor,
        }
    };

    let chart = new ApexCharts(document.querySelector("#new-customers"), options);
    chart.render();

    // 创建 WebSocket 连接
    const ws = new WebSocket(`ws://${serverIp}/total_nineth_counts`);

    // 处理从服务器收到的数据
    ws.onmessage = function(event) {
        let data = JSON.parse(event.data);
        chart.updateOptions({
            series: [{
                data: data.data_counts
            }],
            xaxis: {
                categories: data.time
            }
        });
    };

    // 处理 WebSocket 错误
    ws.onerror = function(error) {
        console.error('WebSocket Error: ', error);
    };
}

newCustomers();


    function customerRating() {
        let options = {
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
                width: 3,
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

    customerRating();

    $(document).on('click', '.select-all', function () {
        let that = $(this),
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

    $(document).on('click', '#customers input[type="checkbox"]', function () {
        let that = $(this);

        if (that.prop('checked')) {
            that.closest('tr').addClass('tr-selected');
        } else {
            that.closest('tr').removeClass('tr-selected');
        }
    });
// 全局变量
var currentPage = 1; // 当前页码
var pageSize = 10; // 每页显示的行数

// 更新表格显示
function updateTable(data) {
    const tbody = document.querySelector("#customerData");
    tbody.innerHTML = ""; // 清空表格内容

    // 计算当前页的起始索引和结束索引
    var startIndex = (currentPage - 1) * pageSize;
    var endIndex = Math.min(startIndex + pageSize, data.length);

    // 遍历接收到的消息并动态创建表格行
    for (let i = startIndex; i < endIndex; i++) {
        const item = data[i];
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>
                <input class="form-check-input" type="checkbox">
            </td>
            <td>
                <a href="#">#${i + 1}</a>
            </td>
            <td>${item.collection_name}</td>
            <td>${item.Domain_Address}</td>
            <td>${item.Remote_Domain}</td>
            <td>${item.toName}</td>
            <td>${item.Timestamp}</td>
            <td>
                <span class="badge bg-success">${item.Domain_Type}</span>
            </td>
            <td class="text-end">
                <div class="d-flex">
                    <div class="dropdown ms-auto">
                        <a href="#" data-bs-toggle="dropdown" class="btn btn-floating" aria-haspopup="true"
                            aria-expanded="false">
                            <i class="bi bi-three-dots"></i>
                        </a>
                        <div class="dropdown-menu dropdown-menu-end">
                            <a href="#" class="dropdown-item">Show</a>
                            <a href="#" class="dropdown-item">Edit</a>
                            <a href="#" class="dropdown-item">Delete</a>
                        </div>
                    </div>
                </div>
            </td>`;
        tbody.appendChild(tr); // 添加表格行到表格中
    }
}

// 建立 WebSocket 连接
var ws = new WebSocket(`ws://${serverIp}/websocket_last_messages`);

// 监听消息事件
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updateTable(data);
};

// 监听错误事件
ws.onerror = function(error) {
    console.error("WebSocket error: " + error.message);
};

// 监听连接关闭事件
ws.onclose = function(event) {
    if (event.wasClean) {
        console.log("WebSocket connection closed cleanly, code=" + event.code + " reason=" + event.reason);
    } else {
        console.error("WebSocket connection closed unexpectedly");
    }
};

// 点击页码时的事件监听器
document.querySelectorAll(".page-link").forEach(function(pageLink) {
    pageLink.addEventListener("click", function(e) {
        e.preventDefault(); // 阻止默认链接跳转行为
        // 移除当前活动页码的 "active" 类
        document.querySelector(".page-item.active").classList.remove("active");
        // 为点击的页码添加 "active" 类
        this.parentNode.classList.add("active");

        const pageNumber = parseInt(this.textContent); // 获取点击的页码
        if (!isNaN(pageNumber)) {
            currentPage = pageNumber; // 更新当前页码
            // 发送请求或其他操作，获取对应页码的数据
            // 这里假设已经通过 WebSocket 接收到了对应的数据，直接调用 updateTable 方法更新表格显示
            // 例如：updateTable(data);
        }
    });
});


});
