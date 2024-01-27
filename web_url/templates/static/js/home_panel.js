/*jshint esversion: 6 */

console.clear();

const defaults = {
	numberGeneratorOptions: {
		dataPoints: 150, // Number of data points to generate
		interval: 100, // Number of ms between each data point
		initialValue: 1, // Initial data value
		volatility: 0.1, // Maximum percent change that can occur
	},
	ticker: {
		enable: true, // Enable or disable ticker
	},
	margins: {
		x: 5,
		y: 10,
	},
	blur: { // SVG blur filter options
		offset: {
			x: 0,
			y: 0,
		},
		amount: 2,
		opacity: 0.05,
		radius: 10,
	},
	transition: { // D3 transition options
		easing: d3.easeLinear, // https://github.com/d3/d3-ease
	},
};

// Exchange Rate Line Chart class
// @param {string} [el] ID selector for chart
// @param {arr} [data] Sample data
class ExchangeChart {
	constructor(
		selector = '',
		data = []
	) {
		Object.assign(this, defaults);

		this.selector = selector;
		this.el = document.getElementById(this.selector.replace('#', ''));
		this.data = data;
		this.resizeTimer;

		if (
			!this.selector.length ||
			!this.data.length ||
			!this.el
		) {
			if (!this.selector.length) {
				console.log('Error: No target element specified');
			}

			if (!this.el) {
				console.log('Error: Target element not found');
			}

			if (!this.data.length) {
				console.log('Error: No data provided');
			}

			return;
		}

		this.ranges = {};

		this.buildChart();
	}

	buildChart() {
		this.setEvents();
		this.setChartDimensions();
		this.setRanges();
		this.defineLine();
		this.initialiseChart();
		this.renderData(this.data);

		if (this.ticker.enable) {
			this.startTicker();
		}
	}

	setEvents() {
		window.addEventListener('resize', (e) => {
			e.preventDefault();

			clearTimeout(this.resizeTimer);

			this.resizeTimer = setTimeout(() => {
				clearInterval(this.tickerInterval);
				clearTimeout(this.tickerTimeout);

				this.setChartDimensions();

				if (this.ticker.enable) {
					this.startTicker();
				}
			}, 200);
		});

		this.button = document.getElementById('generate');

		this.button.addEventListener('click', (e) => {
			e.preventDefault();

			clearInterval(this.tickerInterval);
			clearTimeout(this.tickerTimeout);

			this.renderData(ExchangeChart.generateSampleData(defaults.numberGeneratorOptions));

			if (this.ticker.enable) {
				this.startTicker();
			}

			return false;
		});
	}

	setChartDimensions() {
		this.dimensions = {
			width: this.el.clientWidth,
			height: this.el.clientHeight,
		};

		if (this.svg) {
			this.svg
				.attr('width', this.dimensions.width)
				.attr('height', this.dimensions.height);

			this.wrapper
				.attr('width', this.dimensions.width)
				.attr('height', this.dimensions.height);
		}
	}

	// Set ranges based on SVG canvas dimensions
	setRanges() {
		this.ranges.x = d3.scaleTime()
			.range([0, this.dimensions.width - this.margins.x]);

		this.ranges.y = d3.scaleLinear()
			.range([this.dimensions.height - (2 * this.margins.y), 0]);
	}

	// Define line function
	defineLine() {
		this.line = d3.line()
			.curve(d3.curveBasis)
			.x((data) => {
				return this.ranges.x(data.date);
			})
			.y((data) => {
				return this.ranges.y(data.value);
			});
	}

	// Set up SVG canvas
	initialiseChart() {
		this.svg = d3.select(this.selector)
			.append('svg')
				.attr('width', this.dimensions.width)
				.attr('height', this.dimensions.height);

		this.wrapper = this.svg
			.append('g')
				.attr('width', this.dimensions.width - this.margins.x)
				.attr('height', this.dimensions.height - (2 * this.margins.y))
				.attr('class', 'wrapper')
				.attr('transform', `translate(0, ${this.margins.y})`);

		// this.buildFilter();
		this.buildGuide();
		this.buildLine();
		this.buildEndCircle();
	}

	buildGuide() {
		// Create inspector guide
		this.wrapper
			.append('line')
				.attr('class', 'guide');
	}

	buildLine() {
		// Create chart line group
		this.wrapper
			.append('g')
				.attr('class', 'data');

		// Create chart line
		this.svg.select('.data')
			.append('path')
				.attr('class', 'line');
	}

	buildEndCircle() {
		// Create circle group
		this.wrapper
			.append('g')
				.attr('class', 'circle');

		// Create inspector circle shadow
		this.svg.select('.circle')
			.append('circle')
				.attr('class', 'circle-shadow')
				.attr('r', `${this.blur.radius}px`);

		// Create inspector circle
		this.svg.select('.circle')
			.append('circle')
				.attr('class', 'circle');
	}

	// Build SVG filters
	buildFilter() {
		this.svg
			.append('defs')
			.append('filter')
				.attr('id', 'shadow')
				.attr('x', '-100%')
				.attr('y', '-100%')
				.attr('width', '300%')
				.attr('height', '300%');

		this.svg.select('#shadow')
			.append('feGaussianBlur')
				.attr('in', 'SourceAlpha')
				.attr('stdDeviation', this.blur.amount);

		this.svg.select('#shadow')
			.append('feOffset')
				.attr('dx', this.blur.offset.x)
				.attr('dy', this.blur.offset.y)
				.attr('result', 'offsetblur');

		this.svg.select('#shadow')
			.append('feComponentTransfer')
			.append('feFuncA')
				.attr('type', 'linear')
				.attr('slope', this.blur.opacity);

		this.svg.select('#shadow')
			.append('feMerge')
			.attr('class', 'merge')
			.append('feMergeNode');

		this.svg.select('.merge')
			.append('feMergeNode')
			.attr('in', 'SourceGraphic');
	}

	// Renders all chart components and populates stats
	// @param {arr} [data] Sample data
	renderData(data) {
		this.data = data;

		// Set domains based on sample data
		this.ranges.x.domain(d3.extent(data, (data) => {
				return data.date;
			})
		);

		this.ranges.y.domain(d3.extent(data, (data) => {
				return data.value;
			})
		);

		this.renderGuide(data);
		this.renderLine(data);
		this.renderCircle(data);
		this.populateStats(data);
	}

	// Renders chart line
	renderLine() {
		this.svg.select('.line')
			.data([this.data])
			.interrupt()
			.transition()
				.duration(this.numberGeneratorOptions.interval * 2.5)
				.attr('d', this.line);
	}

	// Renders circle on latest value
	renderCircle() {
		const x = this.ranges.x(this.data[this.data.length - 1].date);
		const y = this.ranges.y(this.data[this.data.length - 1].value);

		this.point = this.svg.select('.circle')
			.interrupt()
			.transition()
				.duration(this.numberGeneratorOptions.interval * 2.5)
				.attr('transform', `translate(${x}, ${y})`);
	}

	// Renders horizontal guide for latest value
	renderGuide() {
		const y = this.ranges.y(this.data[this.data.length - 1].value);

		this.svg.select('.guide')
			.interrupt()
			.transition()
				.duration(this.numberGeneratorOptions.interval * 2.5)
				.attr('x1', 0)
				.attr('y1', y)
				.attr('x2', this.dimensions.width * 2)
				.attr('y2', y);
	}

	// renderInspector() {
	// 	const posX = d3.mouse()[];
	// }

	// Populates stats based on chart data
	populateStats() {
		const rate = document.getElementsByClassName('rate');
		const value = this.data[this.data.length - 1].value;

		rate[0].innerHTML = ExchangeChart.roundNumber(value, 3, true);
	}

	startTicker() {
		this.tickerTimeout = setTimeout(() => {
			this.tickerInterval = setInterval(() => {
				this.tickData(this.data);
			}, this.numberGeneratorOptions.interval);
		}, 1000);
	}

	// Progresses data and updates chart
	tickData() {
		this.data.shift();
		this.data.push({
			date: ExchangeChart.progressDate(this.data, this.numberGeneratorOptions),
			value: ExchangeChart.progressValue(this.data, this.numberGeneratorOptions),
		});

		this.renderData(this.data);
	}

	// Generate a random data set, accounts for volatility which allows for some nice trend simulation
	// @param {obj} [options] Generator options (see defaults)
	// @returns {arr} [data] Sample data
	//
	// data = [
	// 	{
	// 		date: {dateObject},
	// 		value: {float}
	// 	},
	// 	...
	// ]
	static generateSampleData(options) {
		const data = [];
		let n = options.dataPoints;

		// Set first data point
		data.push({
			date: new Date(Date.now()),
			value: options.initialValue,
		});

		n--;

		// Loop and create remaining data points
		while (n > 0) {
			data.push({
				date: ExchangeChart.progressDate(data, options),
				value: ExchangeChart.progressValue(data, options),
			});

			n--;
		}

		return data;
	}

	// Calculates next date in data set
	// @param {arr} [data] Sample data
	// @param {obj} [options] Generator options
	// @returns {obj} Next date
	static progressDate(data, options) {
		return new Date(new Date(data[data.length - 1].date.getTime() + options.interval));
	}

	// Calculates next value in data set
	// @param {arr} [data] Sample data
	// @param {obj} [options] Generator options
	// @returns {float} Next value
	static progressValue(data, options) {
		const total = options.dataPoints;
		const volatility = options.volatility / 100;

		const random = ExchangeChart.getRandomNumber(0, 1, 3);
		let percentChange = 2 * volatility * random;

		if (percentChange > volatility) {
			percentChange -= 2 * volatility;
		}

		const changeValue = data[data.length - 1].value * percentChange;
		return data[data.length - 1].value + changeValue;
	}

	// Generates a random number
	// @param {int} [min] Minimum number
	// @param {int} [max] Maximum number
	// @param {int} [decimalPlaces] Number of decimal places
	// @returns {float} Random float
	static getRandomNumber(min, max, decimalPlaces) {
		return parseFloat((Math.random() * (max - min) + min).toFixed(decimalPlaces));
	}

	// Rounds a number to specified decimal places
	// @param {float} [n] Number to be rounded
	// @param {int} [decimalPlaces] Number of decimal places
	// @param {bool} [pad] Pad output string with trailing zeroes if required
	// @returns {string} Rounded number string
	static roundNumber(n, decimalPlaces, pad) {
		let rounded = (Math.round(n * Math.pow(10, decimalPlaces)) / Math.pow(10, decimalPlaces)).toString();

		if (pad) {
			let integerLength = rounded.indexOf('.') > -1 ? rounded.indexOf('.') : rounded.length;

			if (rounded.indexOf('-') > -1) {
				integerLength--;
			}

			if (rounded.indexOf('.') === -1) {
				rounded = `${rounded}.`;
			}

			const targetLength = decimalPlaces + integerLength + 1;

			if (rounded.length < targetLength) {
				for (let i = rounded.length; i < targetLength; i++) {
					rounded = `${rounded}0`;
				}
			}
		}

		return rounded;
	}

	static loadJSON(url, success, error) {
		const xhr = new XMLHttpRequest();

		xhr.onreadystatechange = () => {
			if (xhr.readyState === XMLHttpRequest.DONE) {
				if (xhr.status === 200) {
					if (success) {
						success(JSON.parse(xhr.responseText));
					} else {
						if (error) {
							error(xhr);
						}
					}
				} else {
					error(xhr.status);
				}
			}
		};

		xhr.open('GET', url, true);
		xhr.send();
	}
}

const exchangeChart = new ExchangeChart('#chart', ExchangeChart.generateSampleData(defaults.numberGeneratorOptions));
