/* test.js */
var data = [
{ y: '2014', a: 50, b: 90 },
{ y: '2015', a: 65, b: 75 },
{ y: '2016', a: 50, b: 50 },
{ y: '2017', a: 75, b: 60 },
{ y: '2018', a: 80, b: 65 },
{ y: '2019', a: 90, b: 70 },
{ y: '2020', a: 100, b: 75 },
{ y: '2021', a: 115, b: 75 },
{ y: '2022', a: 120, b: 85 },
{ y: '2023', a: 145, b: 85 },
{ y: '2024', a: 160, b: 95 }
];

var areaConfig = {
element: 'area-chart',
data: data,
xkey: 'y',
ykeys: ['a', 'b'],
labels: ['Total Income', 'Total Outcome'],
fillOpacity: 0.6,
hideHover: 'auto',
behaveLikeLine: true,
resize: true,
pointFillColors: ['#ffffff'],
pointStrokeColors: ['black'],
lineColors: ['gray', 'red']
};

var lineConfig = {
element: 'line-chart',
data: data,
xkey: 'y',
ykeys: ['a', 'b'],
labels: ['Total Income', 'Total Outcome'],
lineColors: ['blue', 'green']
};

var barConfig = {
element: 'bar-chart',
data: data,
xkey: 'y',
ykeys: ['a', 'b'],
labels: ['Total Income', 'Total Outcome'],
barColors: ['#f0ad4e', '#d9534f']
};

var stackedConfig = {
element: 'stacked',
data: data,
xkey: 'y',
ykeys: ['a', 'b'],
labels: ['Total Income', 'Total Outcome'],
stacked: true
};

var pieConfig = {
element: 'pie-chart',
data: [
{ label: "Friends", value: 30 },
{ label: "Allies", value: 15 },
{ label: "Enemies", value: 45 },
{ label: "Neutral", value: 10 }
],
colors: ['#428bca', '#5bc0de', '#d9534f', '#5cb85c']
};


Morris.Area(areaConfig);
Morris.Line(lineConfig);
Morris.Bar(barConfig);
Morris.Bar(stackedConfig);
Morris.Donut(pieConfig);