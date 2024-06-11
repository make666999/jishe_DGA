/*右侧图表数据,仅支持一个*/
var nodesM = [
    {
    name: '存储器'
},{
    name: '处理器'
},  {
    name: '服务器'
}
];

//左侧图表数据
var nodes = [{
    name: '采集设备01',
    state: '1'
},
    {
        name: '采集设备002',
        state: '1'
    },
    {
        name: '采集设备02',
        state: '1'
    },
    {
        name: '采集设备1',
        state: '1'
    },
    {
        name: '采集设备2',
        state: '1'
    },
    {
        name: '采集设备3',
        state: '1'
    },
    {
        name: '采集设备4',
        state: '1'
    },
    {
        name: '采集设备5',
        state: '0'
    },
    {
        name: '采集设备6',
        state: '1'
    },

];

var charts = {
    nodes: [],
    links: [],
    linesData: []
};
var x = 0;
var y = 1;
var dataMap = new Map();
var aValue = [];
for (var j = 0; j < nodes.length; j++) {

    if (j % 2 == 0) { //偶数
        aValue = [x, y];
        x += 2;
    } else {
        aValue = [x, y - 2];
        x += 2;
    }
    var node = {
        name: nodes[j].name,
        value: aValue,
        symbolSize: 40,
        // symbol: 'image://images/' + nodes[j].img,
        symbol: 'image://static/image/chart/bd1.png',
        itemStyle: {
            normal: {
                color: '#12b5d0',
                fontSize: 12,
                fontWeight: 'normal'
            }
        }
    };
    dataMap.set(nodes[j].name, aValue);
    charts.nodes.push(node);
}
//中间数据显示
for (var k = 0; k < nodesM.length; k++) {
    var nodeM = {
        name: nodesM[k].name,
        value: [ k * 6 , y - 1], // 调整位置确保存储器位于服务器旁边
        symbolSize: 100,
        symbol: 'image://static/image/chart/'+ nodesM[k].name+".png",
    };
    dataMap.set(nodesM[k].name, [ k * 6 , y - 1]);
    charts.nodes.push(nodeM);
}

//画线
var labelName = '';

for (var i = 0; i < nodes.length; i++) {
    //通过传输状态state 显示传输文字提示
    if (nodes[i].state === '1') {
        labelName = '数据传输中'

    } else {
        labelName = '暂停传输'
    }
    if (i%2==0)
    {
        j=0;
    }
    else {
        j=1;
    }
    var link = {
        source: nodes[i].name,
        target: nodesM[j].name,
        label: {
            normal: {
                show: true,
                formatter: labelName,
                color: '#ed46a2',
                fontSize: 12,
                fontWeight: 'normal'
            }
        },
        lineStyle: {
            normal: {
                color: '#ed46a2',
                width: .5
            }
        }
    };
    charts.links.push(link);

    //判断传输状态1 传输动效改变线条颜色
    if (nodes[i].state === '1') {
        link.lineStyle.normal.color = '#27b0fe';
        link.label.normal.color = '#27b0fe';
        var lines = [{
            coord: dataMap.get(nodes[i].name)
        }, {
            coord: dataMap.get(nodesM[j].name)
        }];
        charts.linesData.push(lines)
    }
}

var nodePairs = [
    { source: '处理器', target: '存储器',formatter:"数据转存"},
    { source: '存储器', target: '处理器',formatter:"数据传输"},
    { source: '处理器', target: '服务器' ,formatter:"数据响应"},
    { source: '服务器', target: '处理器' ,formatter:"数据请求"}
];

for (var i2 = 0; i2 < nodePairs.length; i2++) {
    var pair = nodePairs[i2];
    var link2 = {
        source: pair.source,
        target: pair.target,
        label: {
            normal: {
                show: true,
                formatter: pair.formatter,
                color: '#27b0fe',
                fontSize: 12,
                fontWeight: 'normal'
            }
        },
        lineStyle: {
            normal: {
                color: '#27b0fe',
                width: .5
            }
        }
    };
    charts.links.push(link2);

    var lines2 = [{
        coord: dataMap.get(pair.source)
    }, {
        coord: dataMap.get(pair.target)
    }];
    charts.linesData.push(lines2);
}
option = {
    title: {
        text: '混合部署策略'
    },
//  backgroundColor: "#0e1735",
    xAxis: {
        show: false,
        type: 'value'
    },
    yAxis: {
        show: false,
        type: 'value'
    },
    series: [{
        type: 'graph',
        layout: 'none',
        coordinateSystem: 'cartesian2d',
        symbolSize: 50,
        label: {
            normal: {
                show: true,
                position: 'bottom',
                color: '#ffffff'
            }
        },
        lineStyle: {
            normal: {
                shadowColor: 'none',
                opacity: 1, //尾迹线条透明度
                curveness: .1 //尾迹线条曲直度
            }

        },
        edgeSymbolSize: 8,
        data: charts.nodes,
        links: charts.links,
        itemStyle: {
            normal: {
                label: {
                    show: true,
                    formatter: function (item) {
                        return item.data.name
                    }
                }
            }
        }
    }, {
        name: 'A',
        type: 'lines',
        coordinateSystem: 'cartesian2d',
        effect: {
            show: true,
            period: 5, //箭头指向速度，值越小速度越快
            trailLength: 0.02,
            symbol: 'pin',
            color: '#ffaa5f',
            symbolSize: 10

        },
        lineStyle: {
            color: '#fff',
            curveness: .1 //尾迹线条曲直度
        },
        data: charts.linesData,
        z:1
    }]

};


/*采集拓扑图 chart*/
var dom = document.getElementById("chart_3");
var myChartNM = echarts.init(dom, 'purple-passion');
myChartNM.setOption(option);
// window.onresize = myChartNM.resize;

//添加点击事件
myChartNM.on('click', function (params) {
    // 弹窗打印数据的名称
    if (params.dataType == "node") {
        alert("节点名称：" + params.name);
    } else if (params.dataType == "edge") {
        alert("from：" + params.data.source + "=====to:" + params.data.target);
    }
});