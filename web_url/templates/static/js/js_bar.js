(function(){
var myChart = echarts.init(document.getElementById('table1'));
var option = {
       title: [
      {
  text: "深度学习",
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "15",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
}
   ],
    color: ['#3D91F7', '#61BE67'],
    tooltip: {
        textStyle: {
            fontSize: 12 // 调整工具提示的字体大小
        }
    },
    legend: {
        show: true,
        icon: "circle",
        bottom: 30,
        center: 0,
        itemWidth: 14,
        itemHeight: 14,
        itemGap: 21,
        orient: "horizontal",
        data: ['a', 'b'],
        textStyle: {
            fontSize: 14, // 调整图例的字体大小
            color: '#8C8C8C'
        },
    },
    radar: {
        radius: '80%',
        triggerEvent: true,
        name: {
            textStyle: {
                color: '#fff',
                fontSize: 12, // 调整雷达图名称的字体大小
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        nameGap: '2',
        indicator: [
            { name: '准确率', max: 100 },
            { name: '召回率', max: 100 },
            { name: 'F1分数', max: 100 },
            { name: '误报率', max: 100 },
            { name: '漏报率', max: 100 },
        ],
        splitArea: {
            areaStyle: {
                color: [
                    'rgba(0, 255, 255, 0.1)', 'rgba(0, 255, 255, 0.2)',
                    'rgba(0, 255, 255, 0.3)', 'rgba(0, 255, 255, 0.4)',
                    'rgba(0, 255, 255, 0.5)', 'rgba(0, 255, 255, 0.6)'
                ].reverse()
            }
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(0,0,0,0)'
            }
        },
        splitLine: {
            lineStyle: {
                width: 2,
                color: 'transparent'
            }
        },
    },
    series: [{
        name: '安全作业',
        type: 'radar',
        itemStyle: {
            borderColor: 'rgba(66, 242, 185, 1)',
            color: '#fff',
            borderWidth: 0.2
        },
        areaStyle: {
            normal: {
                color: 'rgba(0, 255, 255, 1)'
            }
        },
        symbolSize: 10,
        lineStyle: {
            normal: {
                color: 'rgba(252,211,3, 1)',
                width: 1
            }
        },
        data: [{
            value: [70, 80, 50, 40, 30, 44, 78, 6],
            name: '作业'
        }]
    }],
     grid: {
        top: '80%' // 调整图案整体向下偏移
    }
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('table2'));
var option = {
       title: [
      {
  text: "机器学习",
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "15",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
}
   ],
    color: ['#3D91F7', '#61BE67'],
    tooltip: {
        textStyle: {
            fontSize: 12 // 调整工具提示的字体大小
        }
    },
    legend: {
        show: true,
        icon: "circle",
        bottom: 30,
        center: 0,
        itemWidth: 14,
        itemHeight: 14,
        itemGap: 21,
        orient: "horizontal",
        data: ['a', 'b'],
        textStyle: {
            fontSize: 14, // 调整图例的字体大小
            color: '#8C8C8C'
        },
    },
    radar: {
        radius: '80%',
        triggerEvent: true,
        name: {
            textStyle: {
                color: '#fff',
                fontSize: 12, // 调整雷达图名称的字体大小
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        nameGap: '2',
        indicator: [
            { name: '准确率', max: 100 },
            { name: '召回率', max: 100 },
            { name: 'F1分数', max: 100 },
            { name: '误报率', max: 100 },
            { name: '漏报率', max: 100 },
        ],
        splitArea: {
            areaStyle: {
                color: [
                    'rgba(0, 255, 255, 0.1)', 'rgba(0, 255, 255, 0.2)',
                    'rgba(0, 255, 255, 0.3)', 'rgba(0, 255, 255, 0.4)',
                    'rgba(0, 255, 255, 0.5)', 'rgba(0, 255, 255, 0.6)'
                ].reverse()
            }
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(0,0,0,0)'
            }
        },
        splitLine: {
            lineStyle: {
                width: 2,
                color: 'transparent'
            }
        },
    },
    series: [{
        name: '安全作业',
        type: 'radar',
        itemStyle: {
            borderColor: 'rgba(66, 242, 185, 1)',
            color: '#fff',
            borderWidth: 0.2
        },
        areaStyle: {
            normal: {
                color: 'rgba(0, 255, 255, 1)'
            }
        },
        symbolSize: 10,
        lineStyle: {
            normal: {
                color: 'rgba(252,211,3, 1)',
                width: 1
            }
        },
        data: [{
            value: [60, 70, 48, 56, 70, 34, 88, 16],
            name: '作业'
        }]
    }],
     grid: {
        top: '80%' // 调整图案整体向下偏移
    }
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('table3'));
var option = {
       title: [
      {
  text: "黑白名单",
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "15",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
}
   ],
    color: ['#3D91F7', '#61BE67'],
    tooltip: {
        textStyle: {
            fontSize: 12 // 调整工具提示的字体大小
        }
    },
    legend: {
        show: true,
        icon: "circle",
        bottom: 30,
        center: 0,
        itemWidth: 14,
        itemHeight: 14,
        itemGap: 21,
        orient: "horizontal",
        data: ['a', 'b'],
        textStyle: {
            fontSize: 14, // 调整图例的字体大小
            color: '#8C8C8C'
        },
    },
    radar: {
        radius: '80%',
        triggerEvent: true,
        name: {
            textStyle: {
                color: '#fff',
                fontSize: 12, // 调整雷达图名称的字体大小
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        nameGap: '2',
        indicator: [
            { name: '准确率', max: 100 },
            { name: '召回率', max: 100 },
            { name: 'F1分数', max: 100 },
            { name: '误报率', max: 100 },
            { name: '漏报率', max: 100 },
        ],
        splitArea: {
            areaStyle: {
                color: [
                    'rgba(0, 255, 255, 0.1)', 'rgba(0, 255, 255, 0.2)',
                    'rgba(0, 255, 255, 0.3)', 'rgba(0, 255, 255, 0.4)',
                    'rgba(0, 255, 255, 0.5)', 'rgba(0, 255, 255, 0.6)'
                ].reverse()
            }
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(0,0,0,0)'
            }
        },
        splitLine: {
            lineStyle: {
                width: 2,
                color: 'transparent'
            }
        },
    },
    series: [{
        name: '安全作业',
        type: 'radar',
        itemStyle: {
            borderColor: 'rgba(66, 242, 185, 1)',
            color: '#fff',
            borderWidth: 0.2
        },
        areaStyle: {
            normal: {
                color: 'rgba(0, 255, 255, 1)'
            }
        },
        symbolSize: 10,
        lineStyle: {
            normal: {
                color: 'rgba(252,211,3, 1)',
                width: 1
            }
        },
        data: [{
            value: [83, 80, 50, 70, 50],
            name: '作业'
        }]
    }],
     grid: {
        top: '80%' // 调整图案整体向下偏移
    }
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('table4'));
var option = {
       title: [
      {
  text: "人工匹配",
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "15",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
}
   ],
    color: ['#3D91F7', '#61BE67'],
    tooltip: {
        textStyle: {
            fontSize: 12 // 调整工具提示的字体大小
        }
    },
    legend: {
        show: true,
        icon: "circle",
        bottom: 30,
        center: 0,
        itemWidth: 14,
        itemHeight: 14,
        itemGap: 21,
        orient: "horizontal",
        data: ['a', 'b'],
        textStyle: {
            fontSize: 14, // 调整图例的字体大小
            color: '#8C8C8C'
        },
    },
    radar: {
        radius: '80%',
        triggerEvent: true,
        name: {
            textStyle: {
                color: '#fff',
                fontSize: 12, // 调整雷达图名称的字体大小
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        nameGap: '2',
        indicator: [
            { name: '准确率', max: 100 },
            { name: '召回率', max: 100 },
            { name: 'F1分数', max: 100 },
            { name: '误报率', max: 100 },
            { name: '漏报率', max: 100 },
        ],
        splitArea: {
            areaStyle: {
                color: [
                    'rgba(0, 255, 255, 0.1)', 'rgba(0, 255, 255, 0.2)',
                    'rgba(0, 255, 255, 0.3)', 'rgba(0, 255, 255, 0.4)',
                    'rgba(0, 255, 255, 0.5)', 'rgba(0, 255, 255, 0.6)'
                ].reverse()
            }
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(0,0,0,0)'
            }
        },
        splitLine: {
            lineStyle: {
                width: 2,
                color: 'transparent'
            }
        },
    },
    series: [{
        name: '安全作业',
        type: 'radar',
        itemStyle: {
            borderColor: 'rgba(66, 242, 185, 1)',
            color: '#fff',
            borderWidth: 0.2
        },
        areaStyle: {
            normal: {
                color: 'rgba(0, 255, 255, 1)'
            }
        },
        symbolSize: 10,
        lineStyle: {
            normal: {
                color: 'rgba(252,211,3, 1)',
                width: 1
            }
        },
        data: [{
             value: [91, 83, 60, 86, 30],
            name: '作业'
        }]
    }],
     grid: {
        top: '80%' // 调整图案整体向下偏移
    }
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('echart1'));
let myData1 = ['2017', '2018', '2019', '2020', '2021', '2022', '2023','2024'];
let hj = [400, 350, 500, 600, 900, 1400, 2200, 3000];
let sn = [350, 500, 450, 300, 200, 650, 800, 1547];
let sw = [300, 320, 350, 380, 410, 440, 470, 500];


var option = {

	tooltip: {
		show: true,
		trigger: 'axis',
		textStyle: {
			color: '#fff',
			fontSize: 14
		},

		axisPointer: {
			lineStyle: {
				color: {
					type: 'linear',
					x: 0,
					y: 0,
					x2: 0,
					y2: 1,
					colorStops: [{
						offset: 0,
						color: 'rgba(0, 255, 233,0)'
					}, {
						offset: 0.5,
						color: 'rgba(255, 255, 255,1)',
					}, {
						offset: 1,
						color: 'rgba(0, 255, 233,0)'
					}],
					global: false
				}
			},
		},
		borderColor: "rgba(18, 57, 60, .8)",
		// formatter: "{b}人员类别统计<br>{c}人"
		formatter: function(params, ticket, callback) {
			var htmlStr = '';
			for (var i = 0; i < params.length; i++) {
				var param = params[i];
				var xName = param.name + '各乡镇来渭返谓人数'; //x轴的名称
				var seriesName = param.seriesName; //图例名称
				var value = param.value; //y轴值
				var color = param.color; //图例颜色
				if (i === 0) {
					htmlStr += xName + '<br/>'; //x轴的名称
				}
				htmlStr += '<div>';
				htmlStr +=
					'<span style="margin-right:5px;display:inline-block;width:10px;height:10px;border-radius:5px;background-color:' +
					color + ';"></span>'; //一个点
				htmlStr += seriesName + '：' + value + '人'; //圆点后面显示的文本
				htmlStr += '</div>';
			}
			return htmlStr;
		}
	},
	color: ['#09F6FF', '#3E50FB', '#50D9A5', ],
	legend: {
		// icon: 'circle',
		// itemWidth: 10,
		itemGap: 4,
		x: 'right',
		top: '3%',
		textStyle: {
			color: '#fff',
			fontSize: 13,
			// padding:[0, 6, 0, 6],
		}
	},
	grid: {
		top: '18%',
		left: '1%',
		right: '4%',
		bottom: '2%',
		containLabel: true,
	},
	xAxis: [{
		type: 'category',
		axisLine: {
			lineStyle: {
				color: '#1C82C5'
			}
		},
		axisLabel: {
			interval: 0,
			align: 'center',
			rotate: '40',
			margin: '25',
			textStyle: {
				fontSize: 13,
				color: '#fff'
			}
		},
		splitLine: {
			show: false,
		},
		axisTick: {
			show: false
		},
		boundaryGap: false,
		data: myData1, //this.$moment(data.times).format("HH-mm") ,
	}, ],

	yAxis: [{
		type: 'value',
		min: 0,
		max: 3000,
		splitNumber: 6,
		axisLine: {
			lineStyle: {
				color: '#1C82C5'
			}
		},
		splitLine: {
			show: true,
			lineStyle: {
				color: 'rgba(28, 130, 197, .3)',
				type: 'solid'
			},
		},
		axisLabel: {
			color: '#DEEBFF',
			textStyle: {
				fontSize: 12
			}
		},
		axisTick: {
			show: false
		}
	}, ],
	series: [{
			name: '深度学习',
			type: 'line',
			showSymbol: true,
			symbolSize: 8,
			lineStyle: {
				normal: {
					color: '#09F6FF',
				},
			},
			itemStyle: {
				color: '#09F6FF',
				borderColor: '#09F6FF',
				borderWidth: 2,
			},
			// emphasis: {
			//     itemStyle: {
			//         color: "#fff",
			//         borderColor: "#FF2E2E",
			//         borderWidth: 2,
			//     },
			// },
			areaStyle: {
				normal: {
					color: new echarts.graphic.LinearGradient(
						0,
						0,
						0,
						1,
						[{
								offset: 0,
								color: 'rgba(9, 246, 255, .8)',
							},
							{
								offset: 1,
								color: 'rgba(9, 246, 255, .2)',
							},
						],
						false
					),
				},
			},
			data: hj, //data.values
		},
		{
			name: '机器学习',
			type: 'line',
			showSymbol: true,
			symbolSize: 8,
			lineStyle: {
				normal: {
					color: '#3E50FB',
				},
			},
			itemStyle: {
				color: '#3E50FB',
				borderColor: '#3E50FB',
				borderWidth: 2,
			},
			// emphasis: {
			//     itemStyle: {
			//         color: "#fff",
			//         borderColor: "#F39800",
			//         borderWidth: 2,
			//     },
			// },
			areaStyle: {
				normal: {
					color: new echarts.graphic.LinearGradient(
						0,
						0,
						0,
						1,
						[{
								offset: 0,
								color: 'rgba(62, 80, 251, .8)',
							},
							{
								offset: 1,
								color: 'rgba(62, 80, 251, .2)',
							},
						],
						false
					),
				},
			},
			data: sn, //data.values
		},
		{
			name: '黑白名单',
			type: 'line',
			showSymbol: true,
			symbolSize: 8,
			lineStyle: {
				normal: {
					color: '#50D9A5',
				},
			},
			itemStyle: {
				color: '#50D9A5',
				borderColor: '#50D9A5',
				borderWidth: 2,
			},
			// emphasis: {
			//     itemStyle: {
			//         color: "#fff",
			//         borderColor: "#16D6FF",
			//         borderWidth: 2,
			//     },
			// },
			areaStyle: {
				normal: {
					color: new echarts.graphic.LinearGradient(
						0,
						0,
						0,
						1,
						[{
								offset: 0,
								color: 'rgba(80, 217, 165, .8)',
							},
							{
								offset: 1,
								color: 'rgba(80, 217, 165, .2)',
							},
						],
						false
					),
				},
			},
			data: sw, //data.values
		}
	],
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('echart2'));

var obj = {
    0: '62.25%',
    1: '31.54%',
    2: '22.88%',
    3: '16.77%',
    4: '5.43%',
    5: '0.36%',
    6: '0.03%',
};

option = {
    grid: {
        left: '20%',
        right: '20%',
        bottom: '10%',
        top: '10%'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        },
        formatter: function(params) {
            return params[0].name + ': ' + params[0].value;
        },
        textStyle: {
            color: '#fff' // 设置工具提示文字颜色为白色
        }
    },
    xAxis: {
        axisLabel: {
			textStyle: {
				color: '#fff', // 设置X轴标签文字颜色为白色
				fontSize: 12
			}
		},
		axisLine: {
			 show:false
		},
		splitLine: {
		    show:false
		},
		axisTick: {
		    show:false
		},
        data: ['深度学习','机器学习','黑白名单'],
    },
    yAxis: {
        splitLine: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        axisLabel: {
            show: false
        }
    },
    color: ['#e54035'],
    series: [{
        name: 'hill',
        type: 'pictorialBar',
        barCategoryGap: '-130%',
        symbol: 'path://M0,10 L10,10 C5.5,10 5.5,5 5,0 C4.5,5 4.5,10 0,10 z',
        label: {
            show: true,
            position: 'top',
            distance: 4,
            color: '#fff', // 设置标签文字颜色为白色
            fontSize: 12,
            formatter: function(params) {
                return obj[params.dataIndex];
            }
        },
        itemStyle: {
            normal: {
                color: function(params) {
                    let colorList = [
                        'rgba(124, 116, 238,.7)', 'rgba(60, 103, 215,.7)',
                        'rgba(196, 120, 70,.7)'
                    ];
                    return colorList[params.dataIndex];
                }
            },
            emphasis: {
                opacity: 1
            }
        },
        data: [500, 400, 250],
        z: 10
    }]
};



myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('echart3'));

var option = {
  title: {
    text: 'DGA域名检测方法图',
    textStyle: {
      color: '#fff',
      fontSize: 14
    },
  },
  tooltip: {},
  animationDurationUpdate: 1500,
  animationEasingUpdate: 'quinticInOut',
  series: [
    {
      type: 'graph',
      layout: 'none',
      symbolSize: 60,
      roam: true,
      label: {
        show: true,
        color: '#4381E4'
      },
      edgeSymbolSize: [8, 8],
      edgeLabel: {
        fontSize: 20
      },
      itemStyle: {
        color: '#fff',
        borderColor: '#5E8FC8',
        borderWidth: 2
      },
      data: [
        {
          name: '特征提取',
          x: 0,
          y: 0,
          symbolSize: 70,
          itemStyle: {
            borderColor: '#B1CEF2',
            borderWidth: 6,
            color: '#4381E4',
          },
          label: {
            color: '#fff'
          }
        },
        {
          name: 'NLP',
          x: -100,
          y: -100,
          color: '#5E8FC8'
        },
        {
          name: '统计方法',
          x: 100,
          y: -100
        },
        {
          name: '机器学习',
          x: -100,
          y: 100
        },
        {
          name: '深度学习',
          x: 100,
          y: 100
        },
        {
          name: '词汇一致性',
          x: -200,
          y: -50
        },
        {
          name: '长度变化',
          x: 200,
          y: -50
        },
        {
          name: '元辅音比例',
          x: -200,
          y: 50
        },
        {
          name: '字符频率',
          x: 200,
          y: 50
        },
        {
          name: '随机性评分',
          x: 0,
          y: 200
        }
      ],
      links: [
        {
          source: 'NLP',
          target: '特征提取',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: -0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '统计方法',
          target: '特征提取',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: 0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '特征提取',
          target: '机器学习',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: -0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '特征提取',
          target: '深度学习',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: 0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '词汇一致性',
          target: 'NLP',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: -0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '长度变化',
          target: 'NLP',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: 0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '元辅音比例',
          target: '统计方法',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: -0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '字符频率',
          target: '统计方法',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: 0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '随机性评分',
          target: '机器学习',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: -0.2,
            color: '#5E8FC8'
          }
        },
        {
          source: '随机性评分',
          target: '深度学习',
          symbol: ['', 'arrow'],
          lineStyle: {
            curveness: 0.2,
            color: '#5E8FC8'
          }
        }
      ],
      lineStyle: {
        opacity: 0.9,
        width: 1.5,
        curveness: 0
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          opacity: 1,
          width: 3,
        }
      }
    }
  ]
};




myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();