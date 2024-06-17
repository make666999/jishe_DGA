(function(){
var myChart = echarts.init(document.getElementById('echart1'));
//数据格式[{"value":"1"},{"value":"2"}......],
//在我项目里这里是数据库的一个字段，对这个指标字段进行正太分析
var uploadedDataURL = "/static/data/length.json";

$.getJSON(uploadedDataURL, function (json) {
  let seriesValuedata = json;

  let listData = [];
  let xAxis = [];
  seriesValuedata.forEach((item, index) => {
    listData.push(item.value);
  });

  let objGroup = listData.reduce(function (obj, name) {
    obj[name] = obj[name] ? ++obj[name] : 1;
    return obj;
  }, {});

  let max = Math.max(...listData);
  let min = Math.min(...listData);

  //x轴最大最小前后范围
  let dataRangeMinOP = 2;
  let dataRangeMaXOP = 2.1;
  //间距 ，X轴的步距
  let dataRangeOP = 0.1;
  //小数点位数.这个要和数据精确到哪一位相匹配
  let Xpiont = 1;

  //处理x轴，把数据范围内的x轴求出来，并设置值轴没有的值为空，按顺序对应
  for (
    let i = min - dataRangeMinOP;
    i <= max + dataRangeMaXOP;
    i += dataRangeOP
  ) {
    let str = i.toFixed(Xpiont).toString();
    xAxis.push(str);
    if (objGroup[str] == null) {
      objGroup[str] = 0;
    }
  }


  let barYaxis = [];
  Object.keys(objGroup)
    .sort(function (a, b) {
      return parseFloat(a) - parseFloat(b);
    })
    .map((key) => {
      let num = Math.floor((objGroup[key] / listData.length) * 100 * 100) / 100;
      barYaxis.push(num);
    });

  function sum(array) {
    let s = 0;
    array.forEach(function (val, idx, arr) {
      s += Number(val);
    }, 0);
    return s;
  }

  //正太曲线计算的基本数据和方法
  let avg = 0;
  let stdev = 0;
  avg = sum(listData) / listData.length;

  let sumXY = function (x, y) {
    return Number(x) + Number(y);
  };
  let square = function (x) {
    return Number(x) * Number(x);
  };
  let mean = listData.reduce(sumXY) / listData.length;
  let deviations = listData.map(function (x) {
    return x - mean;
  });

  stdev = Math.sqrt(
    deviations.map(square).reduce(sumXY) / (listData.length - 1)
  );

  //计算正太曲线
  function NDjs(array) {
    let NDarr = [];
    for (let i = 0; i < array.length; i++) {
      let ND =
        Math.sqrt(2 * Math.PI) *
        stdev *
        Math.pow(
          Math.E,
          -(Math.pow(array[i] - avg, 2) / (2 * Math.pow(stdev, 2)))
        );
      NDarr.push(ND);
    }
    return NDarr;
  }
  let lineYaxis = NDjs(xAxis);

  //配置项，本身项目是可以动态在页面配置修改这些属性的，贴到这里用了默认值
  let opacityOption = "off";
  let opacity = 0.5;
  if (opacityOption == "off") {
    opacity = 0;
  }
  let endPositionOption = "all";
  let endPositionPercentum = "";
  let endPosition;
  if (endPositionOption == "all") {
    endPosition = 100;
  } else if (endPositionOption == "third") {
    endPosition = 29;
  } else {
    endPosition = endPositionPercentum;
  }

  let persents = "on";
  let format1;
  let format2;
  if (persents == "on") {
    format1 = "{value} %";
    format2 = "{c} %";
  }

  let data = [];
  let lineDataSet = {
    type: "line",
    smooth: true,
    yAxisIndex: 1,
    areaStyle: {
      opacity: opacity,
    },
    data: lineYaxis,
    name: "分布曲线",
    itemStyle: {
      normal: {
        label: {
          formatter: format2,
          show: false, //开启显示
          position: "top", //在上方显示
          textStyle: {
            //数值样式
            fontSize: 16,
          },
        },
      },
    },
  };
  let barDataSet = {
    type: "bar",
    smooth: true,
    yAxisIndex: 0,
    areaStyle: {
      opacity: opacity,
    },
    data: barYaxis,
    name: "实际分布",
    itemStyle: {
      normal: {
        label: {
          formatter: format2,
          show: false, //开启显示
          position: "top", //在上方显示
          textStyle: {
            //数值样式
            fontSize: 16,
          },
        },
      },
    },
  };
  data.push(lineDataSet, barDataSet);

var option = {
    type: "scroll",
    title: {
      text: "",
      textStyle: {
        color: '#ffffff'  // 设置标题字体颜色为白色
      }
    },
    dataZoom: [
      {
        type: "inside",
        show: false,
        xAxisIndex: [0],
        start: 0,
        end: endPosition,
        borderColor: "#F5A9D0",
        backgroundColor: "#F5A9D0",
      },
      {
        show: false,
        type: "slider",
        xAxisIndex: [0],
        start: 0,
        end: endPosition,
      },
    ],
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
      textStyle: {
        color: '#ffffff'  // 设置提示框字体颜色为白色
      }
    },
    legend: {
      data: ["分布曲线", "实际分布"],
      textStyle: {
        color: '#ffffff'  // 设置图例字体颜色为白色
      }
    },
    xAxis: {
      boundaryGap: false,
      type: "category",
      data: xAxis,
      axisLabel: {
        color: '#ffffff'  // 设置x轴标签字体颜色为白色
      }
    },
    yAxis: [
      {
        type: "value",
        axisLabel: {
          formatter: format1,
          color: '#ffffff'  // 设置y轴标签字体颜色为白色
        }
      },
      {
        show: false,
        type: "value",
        axisLabel: {
          formatter: "{value} %",
          color: '#ffffff'  // 即使隐藏也设置白色
        },
      },
    ],
    grid: [
      {
        x: "5%",
        y: "10%",
        width: "92%",
        height: "75%",
      },
    ],
    series: data.map(function(seriesItem) {
      return {
        ...seriesItem,
        label: {
          show: true,
          color: '#ffffff'  // 设置系列标签字体颜色为白色
        }
      };
    }),
  };

  myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
});


})(),

(function(){
var myChart = echarts.init(document.getElementById('echart2'));
option = {
    tooltip: {
        trigger: "item",
        formatter: function (params) {
            var name = params.name;
            return (
                '<div style="display:flex; align-items:center;">' +
                '<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:' +
                params.color +
                ';margin-right:5px;"></span>' +
                name +
                ": " +
                params.percent +
                "</div>"
            );
        },
    },
    series: [
        {
            name: "Access From",
            type: "pie",
            radius: ["0%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 100,
                borderColor: "#fff",
                borderWidth: 2,
                textStyle: {
                    color: "#fff" // 设置你想要的颜色值，例如 'red', '#000', 'rgba(0,0,0,0.8)'等
                }
            },
            label: {
                show: false,
                position: "center",
            },
            labelLine: {
                show: true,
            },
            data: [
                    { value: 29, name: ".com" },
                    { value: 25, name: ".net" },
                    { value: 10, name: ".org" },
                    { value: 5, name: ".info" },
                    { value: 3, name: ".biz" },
                    { value: 2, name: ".gov" },
                    { value: 4, name: ".edu" },
                    { value: 5, name: ".mil" },
                    { value: 8, name: ".eu" },
                    { value: 7, name: ".co" }
                ],
            label: {
                show: true,
                formatter: function (params) {
                    var name = params.name;
                    var percent = params.percent;
                    return name + "\n" + percent;
                },
            },
        },
    ],
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})(),

(function(){
    var myChart = echarts.init(document.getElementById('echart3'));

    // 假设的每个字母的出现次数（随机生成或实际统计数据）
    const alphabetData = {
        'A': 120, 'B': 105, 'C': 134, 'D': 99, 'E': 140,
        'F': 122, 'G': 88, 'H': 130, 'I': 121, 'J': 77,
        'K': 94, 'L': 111, 'M': 123, 'N': 114, 'O': 132,
        'P': 104, 'Q': 69, 'R': 137, 'S': 128, 'T': 135,
        'U': 97, 'V': 73, 'W': 106, 'X': 65, 'Y': 92, 'Z': 58
    };

    const xData = Object.keys(alphabetData);
    const yData = Object.values(alphabetData).map((value, index) => ({
        count: value,
        value: value
    }));

    const maxNum = Math.max(...Object.values(alphabetData));

    const option = {
        grid: {
            show: false,
            left: "0",
            right: "5%",
            bottom: "0",
            top: "14px",
            containLabel: true,
        },
        xAxis: {
            show: false,
            type: "value",
            max: maxNum + maxNum / 10,
        },
        yAxis: {
            type: "category",
            inverse: true,
            triggerEvent: true,
            axisLabel: {
                show: true,
                fontSize: "12",
                color: "#ffffff",
            },
            splitLine: {
                show: false,
            },
            axisTick: {
                show: false,
            },
            axisLine: {
                show: false,
            },
            data: xData,
        },
        series: [
            {
                type: "bar",
                showBackground: true,
                backgroundStyle: {
                    color: "rgba(180, 180, 180, 0.2)",
                    borderRadius: 20,
                },
                label: {
                    show: true,
                    position: "right",
                    distance: 0,
                    color: "#ffffff",

                    rich: {
                        a: {
                            padding: [0, 0, 0, 5],
                        },
                    },
                },
                itemStyle: {
                    borderRadius: 20,
                    color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                        {
                            offset: 1,
                            color: "rgba(90, 192, 233, 0.04)",
                        },
                        {
                            offset: 0,
                            color: "#5AC0E9",
                        },
                    ]),
                },
                emphasis: {
                    label: {
                        color: "#E9BB5A",
                    },
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                            {
                                offset: 1,
                                color: "rgba(245, 247, 250, 0.04)",
                            },
                            {
                            offset: 0,
                            color: "#E9BB5A",
                            },
                        ]),
                    },
                },
                barWidth: 10,
                data: yData,
            },
        ],
    };

    myChart.setOption(option);
    window.addEventListener("resize",function(){
            myChart.resize();
        });
})();


(function(){
var myChart = echarts.init(document.getElementById('echart4'));
var option = {

	color: ['#3D91F7', '#61BE67'],
	tooltip: {},
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
			fontSize: '70%',
			color: '#8C8C8C'
		},
	},

	radar: {
		// shape: 'circle',
		radius: '80%',
		triggerEvent: true,
		name: {
			textStyle: {
				color: '#fff',
				fontSize: '14',
				borderRadius: 3,
				padding: [3, 5]
			}
		},
		nameGap: '2',
		indicator: [
			{ name: '中国', max: 10 },
			{ name: '美国', max: 10 },
			{ name: '澳大利亚', max: 10 },
			{ name: '日本', max: 10 },
			{ name: '瑞典', max: 10 },
			{ name: '德国', max: 10 },
			{ name: '俄罗斯', max: 10 },

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
		// axisLabel:{//展示刻度
		//     show: true
		// },
		axisLine: { //指向外圈文本的分隔线样式
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
			value: [7, 2, 4, 5, 1, 3, 0, 6],
			name: '作业',



		}
		]
	}]
}
myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();

(function(){
var myChart = echarts.init(document.getElementById('echart5'));
myChart.showLoading();

$.get('/static/data/guanxi.json', function (graph) {
  myChart.hideLoading();
  graph.nodes.forEach(function (node) {
    node.symbolSize = 5;
  });
option = {
    title: {
      text: '非线性分布关系',
      subtext: 'Default layout',
      top: 'bottom',
      left: 'right',
      textStyle: {
        color: '#ffffff'  // 设置标题和副标题字体颜色为白色
      },
      subtextStyle: {
        color: '#ffffff'  // 确保副标题也是白色
      }
    },
    tooltip: {
      textStyle: {
        color: '#ffffff'  // 设置提示框字体颜色为白色
      }
    },
    legend: [
      {
        // selectedMode: 'single',
        data: graph.categories.map(function (a) {
          return a.name;
        }),
        textStyle: {
          color: '#ffffff'  // 设置图例字体颜色为白色
        }
      }
    ],
    series: [
      {
        name: 'Les Miserables',
        type: 'graph',
        layout: 'force',
        data: graph.nodes,
        links: graph.links,
        categories: graph.categories,
        roam: true,
        label: {
          position: 'right',
          color: '#ffffff'  // 设置系列中的标签字体颜色为白色
        },
        force: {
          repulsion: 100
        },
        zoom: 2.4,
      }
    ]
};

  myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
});

})();

(function(){
var myChart = echarts.init(document.getElementById('table1'));
const newData = {
   value: 50000,
   name: "域名数据总数",
   max: 100000,
}
var option = {
   //你的代码

   title: [
      {
  text: newData.name,
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "20",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
},

      {
         text: newData.value,
         x: "49%",
         y: "40%",
         textAlign: "center",
         textStyle: {
            fontWeight: "normal",
            fontSize: "20",
            fontFamily: "SourceHanSansCN-Medium",
            color: "#66FFFF",
         },
      },
   ],
   angleAxis: {
      show: false,

      max: (newData.max * 360) / 270, //-45度到225度，二者偏移值是270度除360度

      type: "value",

      startAngle: 225, //极坐标初始角度

      splitLine: {
         show: false,
      },
   },

   barMaxWidth: 18, //圆环宽度

   radiusAxis: {
      show: false,

      type: "category",
   },

   //圆环位置和大小

   polar: {
      center: ["50%", "50%"],

      radius: "120%",
   },
   series: [
      // 最外层圆环形
      {
         type: "gauge",
         radius: "92%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 1, //刻度的宽度
            },
            length: 25, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: false,
         },
         //刻度线文字
         axisLabel: {
            show: false,
         },
         pointer: {
            show: false,
         },

         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      // 第二层带分界线圆环
      {
         type: "gauge",
         radius: "75%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 2, //刻度的宽度
               shadowColor: "#67FFFC",
               shadowBlur: 1,
            },
            length: 4, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: true,
            length: -15, //长度
            distance: 11,
            lineStyle: {
               color: "#66FFFF",
               width: 3,
            },
         },
         // 刻度线文字
         axisLabel: {
         	show: false,
         	// color: "#fff",
         	// fontSize: 10,
         	// distance: 10,
         },
         data: [
            {
               value: newData.value,
               name: "SCORE",
               itemStyle: {
                  color: "#103781",
               },
            },
         ],
         pointer: {
            show: false,
            length: "12%",
            radius: "50%",
            width: 10, //指针粗细
            offsetCenter: [0, -273],
         },
         detail: {
            show: false,
         },
         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      {
         type: "bar",

         data: [
            {
               //上层圆环，显示数据

               value: newData.value,

               // itemStyle: {
               // 	// color: "#1598FF",
               // },
            },
         ],
         itemStyle: {
            borderRadius: "50%",

            opacity: 1,
            color: {
               type: "linear",
               x: 0,
               y: 0,
               x2: 0,
               y2: 1,
               colorStops: [
                  {
                     offset: 0,
                     color: "rgba(95, 186, 255, 0.2)", // 0% 处的颜色
                  },
                  {
                     offset: 1,
                     color: "rgba(13, 86, 234, 1)", // 100% 处的颜色
                  },
               ],
               global: false, // 缺省为 false
            },
         },
         barGap: "-100%", //柱间距离,上下两层圆环重合

         coordinateSystem: "polar",

         roundCap: true, //顶端圆角

         z: 3, //圆环层级，同zindex
      },
      {
         //下层圆环，显示最大值

         type: "bar",

         data: [
            {
               value: newData.max,

               itemStyle: {
                  color: "#1598FF",

                  opacity: 0.2,

                  borderWidth: 0,
               },
            },
         ],

         barGap: "-100%",

         coordinateSystem: "polar",

         roundCap: true,

         z: 1,
      },
   ],
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('table2'));
const newData = {
   value: 34,
   name: "DGA域名种类",
   max: 100,
}
var option = {
   //你的代码

   title: [
      {
  text: newData.name,
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "20",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
},

      {
         text: newData.value,
         x: "49%",
         y: "35%",
         textAlign: "center",
         textStyle: {
            fontWeight: "normal",
            fontSize: "40",
            fontFamily: "SourceHanSansCN-Medium",
            color: "#66FFFF",
         },
      },
   ],
   angleAxis: {
      show: false,

      max: (newData.max * 360) / 270, //-45度到225度，二者偏移值是270度除360度

      type: "value",

      startAngle: 225, //极坐标初始角度

      splitLine: {
         show: false,
      },
   },

   barMaxWidth: 18, //圆环宽度

   radiusAxis: {
      show: false,

      type: "category",
   },

   //圆环位置和大小

   polar: {
      center: ["50%", "50%"],

      radius: "120%",
   },
   series: [
      // 最外层圆环形
      {
         type: "gauge",
         radius: "92%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 1, //刻度的宽度
            },
            length: 25, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: false,
         },
         //刻度线文字
         axisLabel: {
            show: false,
         },
         pointer: {
            show: false,
         },

         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      // 第二层带分界线圆环
      {
         type: "gauge",
         radius: "75%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 2, //刻度的宽度
               shadowColor: "#67FFFC",
               shadowBlur: 1,
            },
            length: 4, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: true,
            length: -15, //长度
            distance: 11,
            lineStyle: {
               color: "#66FFFF",
               width: 3,
            },
         },
         // 刻度线文字
         axisLabel: {
         	show: false,
         	// color: "#fff",
         	// fontSize: 10,
         	// distance: 10,
         },
         data: [
            {
               value: newData.value,
               name: "SCORE",
               itemStyle: {
                  color: "#103781",
               },
            },
         ],
         pointer: {
            show: false,
            length: "12%",
            radius: "50%",
            width: 10, //指针粗细
            offsetCenter: [0, -273],
         },
         detail: {
            show: false,
         },
         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      {
         type: "bar",

         data: [
            {
               //上层圆环，显示数据

               value: newData.value,

               // itemStyle: {
               // 	// color: "#1598FF",
               // },
            },
         ],
         itemStyle: {
            borderRadius: "50%",

            opacity: 1,
            color: {
               type: "linear",
               x: 0,
               y: 0,
               x2: 0,
               y2: 1,
               colorStops: [
                  {
                     offset: 0,
                     color: "rgba(95, 186, 255, 0.2)", // 0% 处的颜色
                  },
                  {
                     offset: 1,
                     color: "rgba(13, 86, 234, 1)", // 100% 处的颜色
                  },
               ],
               global: false, // 缺省为 false
            },
         },
         barGap: "-100%", //柱间距离,上下两层圆环重合

         coordinateSystem: "polar",

         roundCap: true, //顶端圆角

         z: 3, //圆环层级，同zindex
      },
      {
         //下层圆环，显示最大值

         type: "bar",

         data: [
            {
               value: newData.max,

               itemStyle: {
                  color: "#1598FF",

                  opacity: 0.2,

                  borderWidth: 0,
               },
            },
         ],

         barGap: "-100%",

         coordinateSystem: "polar",

         roundCap: true,

         z: 1,
      },
   ],
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('table3'));
const newData = {
   value: 80,
   name: "DGA域名最大长度",
   max: 100,
}
var option = {
   //你的代码

   title: [
      {
  text: newData.name,
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "20",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
},

      {
         text: newData.value,
         x: "49%",
         y: "35%",
         textAlign: "center",
         textStyle: {
            fontWeight: "normal",
            fontSize: "40",
            fontFamily: "SourceHanSansCN-Medium",
            color: "#66FFFF",
         },
      },
   ],
   angleAxis: {
      show: false,

      max: (newData.max * 360) / 270, //-45度到225度，二者偏移值是270度除360度

      type: "value",

      startAngle: 225, //极坐标初始角度

      splitLine: {
         show: false,
      },
   },

   barMaxWidth: 18, //圆环宽度

   radiusAxis: {
      show: false,

      type: "category",
   },

   //圆环位置和大小

   polar: {
      center: ["50%", "50%"],

      radius: "120%",
   },
   series: [
      // 最外层圆环形
      {
         type: "gauge",
         radius: "92%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 1, //刻度的宽度
            },
            length: 25, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: false,
         },
         //刻度线文字
         axisLabel: {
            show: false,
         },
         pointer: {
            show: false,
         },

         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      // 第二层带分界线圆环
      {
         type: "gauge",
         radius: "75%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 2, //刻度的宽度
               shadowColor: "#67FFFC",
               shadowBlur: 1,
            },
            length: 4, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: true,
            length: -15, //长度
            distance: 11,
            lineStyle: {
               color: "#66FFFF",
               width: 3,
            },
         },
         // 刻度线文字
         axisLabel: {
         	show: false,
         	// color: "#fff",
         	// fontSize: 10,
         	// distance: 10,
         },
         data: [
            {
               value: newData.value,
               name: "SCORE",
               itemStyle: {
                  color: "#103781",
               },
            },
         ],
         pointer: {
            show: false,
            length: "12%",
            radius: "50%",
            width: 10, //指针粗细
            offsetCenter: [0, -273],
         },
         detail: {
            show: false,
         },
         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      {
         type: "bar",

         data: [
            {
               //上层圆环，显示数据

               value: newData.value,

               // itemStyle: {
               // 	// color: "#1598FF",
               // },
            },
         ],
         itemStyle: {
            borderRadius: "50%",

            opacity: 1,
            color: {
               type: "linear",
               x: 0,
               y: 0,
               x2: 0,
               y2: 1,
               colorStops: [
                  {
                     offset: 0,
                     color: "rgba(95, 186, 255, 0.2)", // 0% 处的颜色
                  },
                  {
                     offset: 1,
                     color: "rgba(13, 86, 234, 1)", // 100% 处的颜色
                  },
               ],
               global: false, // 缺省为 false
            },
         },
         barGap: "-100%", //柱间距离,上下两层圆环重合

         coordinateSystem: "polar",

         roundCap: true, //顶端圆角

         z: 3, //圆环层级，同zindex
      },
      {
         //下层圆环，显示最大值

         type: "bar",

         data: [
            {
               value: newData.max,

               itemStyle: {
                  color: "#1598FF",

                  opacity: 0.2,

                  borderWidth: 0,
               },
            },
         ],

         barGap: "-100%",

         coordinateSystem: "polar",

         roundCap: true,

         z: 1,
      },
   ],
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();
(function(){
var myChart = echarts.init(document.getElementById('table4'));
const newData = {
   value: 32,
   name: "DGA分布出现国家数",
   max: 100,
}
var option = {
   //你的代码

   title: [
      {
  text: newData.name,
  x: "50%",
  y: "bottom", // 将y属性设置为bottom
  textAlign: "center",
  textStyle: {
    fontWeight: "normal",
    fontSize: "20",
    fontFamily: "SourceHanSansCN-Medium",
    color: "#ffffff",
  },
},

      {
         text: newData.value,
         x: "49%",
         y: "35%",
         textAlign: "center",
         textStyle: {
            fontWeight: "normal",
            fontSize: "40",
            fontFamily: "SourceHanSansCN-Medium",
            color: "#66FFFF",
         },
      },
   ],
   angleAxis: {
      show: false,

      max: (newData.max * 360) / 270, //-45度到225度，二者偏移值是270度除360度

      type: "value",

      startAngle: 225, //极坐标初始角度

      splitLine: {
         show: false,
      },
   },

   barMaxWidth: 18, //圆环宽度

   radiusAxis: {
      show: false,

      type: "category",
   },

   //圆环位置和大小

   polar: {
      center: ["50%", "50%"],

      radius: "120%",
   },
   series: [
      // 最外层圆环形
      {
         type: "gauge",
         radius: "92%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 1, //刻度的宽度
            },
            length: 25, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: false,
         },
         //刻度线文字
         axisLabel: {
            show: false,
         },
         pointer: {
            show: false,
         },

         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      // 第二层带分界线圆环
      {
         type: "gauge",
         radius: "75%", // 1行3个
         center: ["50%", "50%"],
         splitNumber: 10,
         // min: 0,
         max: 100,

         startAngle: 225,
         endAngle: -45,
         z: 99,

         // 线
         axisLine: {
            lineStyle: {
               width: 1,
               color: [[1, "rgba(255,255,255,0)"]],
            },
            detail: {
               formatter: "{value}",
            },
            data: [
               {
                  value: 50,
                  name: "SCORE",
               },
            ],
         },
         // //刻度标签。
         axisTick: {
            show: true,
            splitNumber: 5, //刻度的段落数
            lineStyle: {
               color: "#103781",
               width: 2, //刻度的宽度
               shadowColor: "#67FFFC",
               shadowBlur: 1,
            },
            length: 4, //刻度的长度
         },
         splitLine: {
            //文字和刻度的偏移量
            show: true,
            length: -15, //长度
            distance: 11,
            lineStyle: {
               color: "#66FFFF",
               width: 3,
            },
         },
         // 刻度线文字
         axisLabel: {
         	show: false,
         	// color: "#fff",
         	// fontSize: 10,
         	// distance: 10,
         },
         data: [
            {
               value: newData.value,
               name: "SCORE",
               itemStyle: {
                  color: "#103781",
               },
            },
         ],
         pointer: {
            show: false,
            length: "12%",
            radius: "50%",
            width: 10, //指针粗细
            offsetCenter: [0, -273],
         },
         detail: {
            show: false,
         },
         title: {
            // 仪表盘标题。
            show: false,
         },
      },
      {
         type: "bar",

         data: [
            {
               //上层圆环，显示数据

               value: newData.value,

               // itemStyle: {
               // 	// color: "#1598FF",
               // },
            },
         ],
         itemStyle: {
            borderRadius: "50%",

            opacity: 1,
            color: {
               type: "linear",
               x: 0,
               y: 0,
               x2: 0,
               y2: 1,
               colorStops: [
                  {
                     offset: 0,
                     color: "rgba(95, 186, 255, 0.2)", // 0% 处的颜色
                  },
                  {
                     offset: 1,
                     color: "rgba(13, 86, 234, 1)", // 100% 处的颜色
                  },
               ],
               global: false, // 缺省为 false
            },
         },
         barGap: "-100%", //柱间距离,上下两层圆环重合

         coordinateSystem: "polar",

         roundCap: true, //顶端圆角

         z: 3, //圆环层级，同zindex
      },
      {
         //下层圆环，显示最大值

         type: "bar",

         data: [
            {
               value: newData.max,

               itemStyle: {
                  color: "#1598FF",

                  opacity: 0.2,

                  borderWidth: 0,
               },
            },
         ],

         barGap: "-100%",

         coordinateSystem: "polar",

         roundCap: true,

         z: 1,
      },
   ],
};

myChart.setOption(option);
window.addEventListener("resize",function(){
            myChart.resize();
        });
})();