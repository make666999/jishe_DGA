
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
        data: ['04-18','04-19','04-20','04-21','04-22','4-23'],
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
        name: '数量',
        type: 'line',
        data: [23,60,20,36,23,85],
        lineStyle: {
            normal: {
                width: 8,
                color: {
                    type: 'linear',

                    colorStops: [{
                        offset: 0,
                        color: '#8e9ff5' // 0% 处的颜色
                    }, {
                        offset: 1,
                        color: '#ad97e5' // 100% 处的颜色
                    }],
                    globalCoord: false // 缺省为 false
                },
                shadowColor: 'rgba(79,79,145,0.79)',
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
                borderColor: "#c887f3"
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
        container.style.backgroundColor = "#D1C4E9"; // 激活颜色
        dataUsageText.textContent = "开启"; // 激活文本
    } else {
        container.style.backgroundColor = "#f3f3f3"; // 原始颜色
        dataUsageText.textContent = "关闭"; // 关闭文本
    }
}
const levels = {
        '安全等级': ['低', '中', '高'],
        '漏洞预警': ['低', '中', '高'],
        '风险巡航': ['低', '中', '高'],
        '策略偏向': ['保守', '均衡', '积极']
    };
// 当文档加载完毕

async function sendSettingToBackend(code_type, deploymentType) {
    deploymentType=deploymentType.toString()
    const formData = {
        code_types : code_type,
        new_model_value: deploymentType
    };

    const response = await fetch('/api/send_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    const data = await response.json();
    console.log(data);  // 弹出后端返回的消息
}


document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.custom-info-box').forEach(box => {
        const title = box.querySelector('.info-box-title').textContent;
        const content = box.querySelector('.info-box-content');

        const decreaseButton = box.querySelector('.decrease');
        const increaseButton = box.querySelector('.increase');

        const updateSwitches = () => {
            const securityLevel = content.textContent.trim();
            const switches = document.querySelectorAll('.features-container .feature-item .switch input[type="checkbox"]');

            switches.forEach((sw, index) => {
                if (securityLevel === '高') {
                    sw.checked = true;
                } else if (securityLevel === '中') {
                    sw.checked = index < 2;
                } else if (securityLevel === '低') {
                    sw.checked = false;
                }
                toggleFeature(sw, sw.getAttribute('id').replace('toggleSwitch', 'dataUsage'));
            });
        };

        const handleLevelChange = () => {

            const currentLevelIndex = levels[title].indexOf(content.textContent.trim());

            if (title === "安全等级") {
                if (currentLevelIndex > 0) {
                    content.textContent = levels[title][currentLevelIndex - 1];
                    updateSwitches(); // 更新开关状态
                    console.log(content.textContent);

                    sendSettingToBackend(title, currentLevelIndex - 1);
                }
            } else {
                if (currentLevelIndex > 0) {
                     content.textContent = levels[title][currentLevelIndex - 1];
                sendSettingToBackend(title, currentLevelIndex -1);

                }
            }
        };

        const handleLevelIncrease = () => {
            const currentLevelIndex = levels[title].indexOf(content.textContent.trim());

            if (title === "安全等级") {
                if (currentLevelIndex < levels[title].length - 1) {
                    content.textContent = levels[title][currentLevelIndex + 1];
                    updateSwitches(); // 更新开关状态
                sendSettingToBackend(title, currentLevelIndex + 1); // 发送设置到后端，第一个参数是标题，第二个参数是当前级别索引加二
                }
            } else {
                if (currentLevelIndex < levels[title].length - 1) {
                    content.textContent = levels[title][currentLevelIndex + 1];
                sendSettingToBackend(title, currentLevelIndex + 1); // 发送设置到后端，第一个参数是标题，第二个参数是当前级别索引加二
                }
            }
        };

        decreaseButton.onclick = handleLevelChange;
        increaseButton.onclick = handleLevelIncrease;
    });
});





