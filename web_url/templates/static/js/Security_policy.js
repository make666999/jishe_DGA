
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





var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var raf = requestAnimationFrame;
var TAU = Math.PI * 2;

var W = canvas.width = window.innerHeight/5;
var H = canvas.height = window.innerHeight/5;
var cX = W/2;//center point x
var cY = H/2;//center point y
var i = 0;
var alpha;
var rad = H/2;
function Rardar(){
  i += 1;
  if(i==360)
    i = 0;
  alpha = TAU*i/360;
  ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
  ctx.fillRect(0,0,W,H);

  ctx.strokeStyle = 'rgba(0, 255, 255, 1)';
  ctx.beginPath();
  ctx.moveTo(cX,cY);
  ctx.lineTo(cX+Math.cos(alpha)*rad,cY+Math.sin(alpha)*rad);
  ctx.stroke();
	window.setTimeout(Rardar, 10);
}
raf(Rardar);




var lineChart = echarts.init(document.getElementById('lineChart'));
option = {
    tooltip: {
        trigger: 'axis'
    },
    xAxis: [{
        type: 'category',
        data: ['03-21','03-22','03-23','03-24','03-25','03-26'],
        axisLine: {
            lineStyle: {
                color: "#999"
            }
        }
    }],
    yAxis: [{
        type: 'value',
        splitNumber: 4,
        splitLine: {
            lineStyle: {
                type: 'dashed',
                color: '#DDD'
            }
        },
        axisLine: {
            show: false,
            lineStyle: {
                color: "#333"
            },
        },
        nameTextStyle: {
            color: "#999"
        },
        splitArea: {
            show: false
        }
    }],
    series: [{
        name: '课时',
        type: 'line',
        data: [23,60,20,36,23,85],
        lineStyle: {
            normal: {
                width: 8,
                color: {
                    type: 'linear',

                    colorStops: [{
                        offset: 0,
                        color: '#A9F387' // 0% 处的颜色
                    }, {
                        offset: 1,
                        color: '#48D8BF' // 100% 处的颜色
                    }],
                    globalCoord: false // 缺省为 false
                },
                shadowColor: 'rgba(72,216,191, 0.3)',
                shadowBlur: 10,
                shadowOffsetY: 20
            }
        },
        itemStyle: {
            normal: {
                color: '#fff',
                borderWidth: 10,
                /*shadowColor: 'rgba(72,216,191, 0.3)',
                shadowBlur: 100,*/
                borderColor: "#A9F387"
            }
        },
        smooth: true
    }]
};

// Use the 'lineChart' instance to set the option
option && lineChart.setOption(option);


function toggleFeature(element, dataUsageId) {
    var container = element.closest('.feature-item');
    var dataUsageText = document.getElementById(dataUsageId);

    if (element.checked) {
        container.style.backgroundColor = "#D1C4E9"; // 设置为你的激活颜色
        dataUsageText.textContent = "开启"; // 更改为你的激活文本
    } else {
        container.style.backgroundColor = "#f3f3f3"; // 恢复原始颜色
        // 根据 dataUsageId 来决定文本是显示“关闭”还是“未激活”
        dataUsageText.textContent = (dataUsageId === 'dataUsage1') ? "关闭" : "未激活";
    }
}

// 当文档加载完毕
// 当文档加载完毕
document.addEventListener('DOMContentLoaded', () => {
    // 安全等级改变时的逻辑
    document.querySelectorAll('.info-box-button').forEach(button => {
        button.addEventListener('click', function() {
            // 获取当前的安全等级
            const securityLevel = document.getElementById('securityLevel').textContent;
            const switches = document.querySelectorAll('.features-container .feature-item .switch input[type="checkbox"]');

            // 根据安全等级设置开关状态
            switches.forEach(sw => {
                if (securityLevel === '高' && sw.id === 'toggleSwitch1') {
                    sw.checked = true; // 只打开系统通知
                    toggleFeature(sw, sw.getAttribute('id').replace('toggleSwitch', 'dataUsage')); // 更新文本和背景
                } else if (securityLevel === '中' && sw.id !== 'toggleSwitch4') {
                    sw.checked = true; // 打开除了域名拦截外的所有开关
                    toggleFeature(sw, sw.getAttribute('id').replace('toggleSwitch', 'dataUsage')); // 更新文本和背景
                } else if (securityLevel === '低') {
                    sw.checked = false; // 安全等级为低，关闭所有开关
                    toggleFeature(sw, sw.getAttribute('id').replace('toggleSwitch', 'dataUsage')); // 更新文本和背景
                } else {
                    sw.checked = false; // 其他情况，关闭开关
                    toggleFeature(sw, sw.getAttribute('id').replace('toggleSwitch', 'dataUsage')); // 更新文本和背景
                }
            });
        });
    });
});



document.addEventListener('DOMContentLoaded', () => {
   const levels = {
    '安全等级': ['低', '中', '高'],
    '漏洞预警': ['低', '中', '高'],
    '风险巡航': ['低', '中', '高'],
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

