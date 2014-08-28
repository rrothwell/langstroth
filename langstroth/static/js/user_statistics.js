////// Area Plot of NeCTAR User Registration History

//==== Data manipulation

//==== String utilities

var parseDate = d3.time.format("%Y-%m-%d").parse;

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
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var area = d3.svg.area()
    .x(function(d) { return x(d.date); })
    .y0(HEIGHT)
    .y1(function(d) { return y(d.count); });

var svg = d3.select("#plot-area").append("svg")
    .attr("width", WIDTH + MARGIN.LEFT + MARGIN.RIGHT)
    .attr("height", HEIGHT + MARGIN.TOP + MARGIN.BOTTOM)
  .append("g")
    .attr("transform", "translate(" + MARGIN.LEFT + "," + MARGIN.TOP + ")");

function visualise(data) {
	
	  x.domain(d3.extent(data, function(d) { return d.date; }));
	  y.domain([0, d3.max(data, function(d) { return d.count; })]);

	  svg.append("path")
	      .datum(data)
	      .attr("class", "area")
	      .attr("d", area);

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + HEIGHT + ")")
	      .call(xAxis);

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

function processResponse(registrationFrequency) {
	registrationFrequency.forEach(function(record) {
		record.date = parseDate(record.date);
		record.count = +record.count;
	  });
}

function load() {
	d3.json("/user_statistics/rest/registrations/frequency", function(error, registrationFrequency) {
		processResponse(registrationFrequency);
		visualise(registrationFrequency);
	});
}

load();



