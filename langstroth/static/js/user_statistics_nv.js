var registrationFrequency = [];
var isCumulative = true;

var dateFormat = d3.time.format("%Y-%m-%d");
var parseDate = dateFormat.parse;
var frequencyFormat = d3.format(',.0f');

var svg = d3.select("#plot-area").append("svg");

//---- The render function

function visualise(trend) {
		
	  nv.addGraph(function() {
		    var chart = nv.models.stackedAreaChart()
		                  .margin({right: 100})
		                  .x(function(d) { 
		                	  return d[0].getTime(); 
		                	  })   
		                  .y(function(d) { 
		                	  return d[1]; 
		                	  })  
		                  .useInteractiveGuideline(true) 
		                  .rightAlignYAxis(true) 
		                  .transitionDuration(500)
		                  .showControls(false)
		                  .clipEdge(true);

		    chart.xAxis
		    .tickFormat(function(d) {
		      return dateFormat(new Date(d)) ;
		    });

		    chart.yAxis
		    .tickFormat(frequencyFormat);

			//var path = svg.selectAll("path").data([trend]).call(chart);	
			svg.datum(trend).call(chart);	

		    nv.utils.windowResize(chart.update);

		    return chart;
		  });
  
}

function processResponse(registrationFrequency) {
	var trend = [];
	var sum = 0;
	registrationFrequency.forEach(function(record) {
		var item = [];
		item[0] = parseDate(record.date);
		if (isCumulative) {
			sum += +record.count;
			item[1] = sum;
		} else {
			item[1] = +record.count;
		}
		trend.push(item);
	  });

	var wrappedTrend = {};
	wrappedTrend['key'] = 'User Registrations';
	wrappedTrend['values'] = trend;
	return [wrappedTrend];
}

function load() {
	d3.json("/user_statistics/rest/registrations/frequency", function(error, responseData) {
		registrationFrequency = responseData;
		var trend = processResponse(registrationFrequency);
		visualise(trend);
	});
}

load();

function change() {
	$('#graph-buttons button').removeClass('active');
	$(this).addClass('active');
	isCumulative = this.id == 'cumulative';
	var trend = processResponse(registrationFrequency);
	visualise(trend);
}

d3.selectAll("button").on("click", change);


