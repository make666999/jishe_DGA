
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
var option = {

  xAxis: {
    type: 'category',
    data: ['3-19', '3-20', '3-21', '3-22', '3-23', '3-24', '3-25']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [20, 32, 21, 27, 12, 19, 10],
      type: 'line',
      smooth: true
    }
  ]
};

// Use the 'lineChart' instance to set the option
option && lineChart.setOption(option);
