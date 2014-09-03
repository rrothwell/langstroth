////// Area Plot of NeCTAR User Registration History
var registrationFrequency = [];
var isCumulative = false;

//==== Data manipulation

//==== String utilities

var dateFormat = d3.time.format("%Y-%m-%d");
var monthFormat = d3.time.format("%m");
var yearFormat = d3.time.format("%Y");
var parseDate = dateFormat.parse;

//==== Data visualisation

//---- Visualisation Constants

var MARGIN = {TOP: 20, RIGHT: 20, BOTTOM: 30, LEFT: 50},
WIDTH = 960 - MARGIN.LEFT - MARGIN.RIGHT,
HEIGHT = 500 - MARGIN.TOP - MARGIN.BOTTOM;

var x = d3.time.scale()
    .range([0, WIDTH]);

var y = d3.scale.linear()
    .range([HEIGHT, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(function(d, i) {
    	var month = d.getMonth();
    	if (month == 0) {
        	return yearFormat(d);
    	} else {
    		return monthFormat(d);
    	}
    });

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var svg = d3.select("#plot-area").append("svg")
    .attr("width", WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
    .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
  .append("g")
    .attr("transform", "translate(" + MARGIN.LEFT + "," + MARGIN.TOP + ")");

var area = d3.svg.area()
    .x(function(d) { return x(d.date); })
    .y0(HEIGHT)
    .y1(function(d) { return y(d.count); });

//---- The render function

function visualise(trend) {

	x.domain(d3.extent(trend, function(d) { 
		return d.date; 
	}));
	y.domain([0, d3.max(trend, function(d) { 
		return d.count;
	})]);
  
	var path = svg.selectAll("path").data([trend]);	
	path.attr("class", "area").attr("d", area);
	path.enter().append("path").attr("class", "area").attr("d", area);
	path.exit().remove();
  
	var xAxisG = svg.selectAll("g.x");
	xAxisG.remove();
	
	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + HEIGHT + ")")
	      .call(xAxis)
	    .append("text")	      
	      .attr("x", WIDTH)
	      .attr("dx", "-0.71em")
	      .attr("dy", "-0.71em")
	      .style("text-anchor", "end")
	      .text("Date");
	  
		var yAxisG = svg.selectAll("g.y");
		yAxisG.remove();

		svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("User registrations");
}

//==== Data loading

function processResponse(registrationFrequency) {
	var trend = [];
	var sum = 0;
	registrationFrequency.forEach(function(record) {
		var item = {};
		item.date = parseDate(record.date);
		if (isCumulative) {
			sum += +record.count;
			item.count = sum;
		} else {
			item.count = +record.count;
		}
		trend.push(item);
	  });
	return trend;
}

function load() {
	d3.json("/user_statistics/rest/registrations/frequency", function(error, responseData) {
		registrationFrequency = responseData;
		var trend = processResponse(registrationFrequency);
		visualise(trend);
	});
}

load();

//==== User Interactions.

function change() {
	$('#graph-buttons button').removeClass('active');
	$(this).addClass('active');
	isCumulative = this.id == 'cumulative';
	var trend = processResponse(registrationFrequency);
	visualise(trend);
}

d3.selectAll("button").on("click", change);


