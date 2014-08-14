////// Project Details Page for NeCTAR Allocations

//==== Details Table

var headings = {
	"start_date" : "Start date",
	"end_date" : "End date",
	"use_case" : " Use case",
	"usage_patterns" : "Usage patterns",
	"instance_quota" : "Instance quota",
	"core_quota" : "Core quota",
	"for_distribution" : "FOR distribution",
	"submit_date" : "Submit date",
	"modified_time" : "Modified time"
};

var toolTip = d3.select("body")
				.append("div")
				.style("position", "absolute")
				.style("z-index", "10")
				.style("visibility", "hidden")
				.style("background-color", "rgba(255,255,255,0.75)")
				.style("padding", "2px 4px 2px 4px")
				.style("border-radius", "3px")
				.text("a simple tooltip");


//==== HTML Table For Project Details.
// Populated on page load. Dynamic update after page load is not supported.

function tabulateSummary(pageAreaSelector, projectSummary, forTranslation) {

	// Define the table with heading.
	var table = d3.select(pageAreaSelector).append("table")
					.attr("class", "table table-striped table-bordered table-condensed");	
	tbody = table.append("tbody"); 

	// Add rows with rows (tr), row headings (th) and the detail entries (td).
	var rows = tbody.selectAll("tr")
					.data(function(row) { 
						var keys = [];
						for (key in headings) {
							keys.push(key);
						} 
						return keys; })
					.enter()
					.append("tr");
	
	rows.append("th")
		.style("min-width", "100px")
		.text(function(row) { 
				return headings[row]; 
			});
	
	rows.append("td")
		.html(function(row) { 
			if (row == "for_distribution") {
				var forDistributionTable = "<table class='table table-striped table-bordered table-condensed'  style='max-width: 40em;'>";
				if (projectSummary.field_of_research_1) {
					var for1 = projectSummary.field_of_research_1; 
					forDistributionTable += "<tr  style='line-height: 1.0;'>"
					+ "<th style='min-width: 6em'>" + "FOR&nbsp;1:&nbsp;</th>"
					+ "<td style='min-width: 20em'>" + forTranslation[for1] + "&nbsp;(" + for1 + ")</td>"
					+ "<td style='max-width: 4em'>" + projectSummary.for_percentage_1 + "&nbsp;%&nbsp;</td>"
					+ "</tr>";
				}
				if (projectSummary.field_of_research_2) {
					var for2 = projectSummary.field_of_research_2; 
					forDistributionTable += "<tr style='line-height: 1.0;'>"
					+ "<th style='min-width: 6em'>" + "FOR&nbsp;2:&nbsp;</th>"
					+ "<td style='min-width: 20em'>" + forTranslation[for2] + "&nbsp;(" + for2 + ")</td>"
					+ "<td style='max-width: 4em'>" + projectSummary.for_percentage_2 + "&nbsp;%&nbsp;</td>"
					+ "</tr>";
				}
				if (projectSummary.field_of_research_3) {
					var for3 = projectSummary.field_of_research_3; 
					forDistributionTable += "<tr style='line-height: 1.0;'>"
					+ "<th style='min-width: 6em'>" + "FOR&nbsp;3:&nbsp;</th>"
					+ "<td style='min-width: 20em'>" + forTranslation[for3] + "&nbsp;(" + for3 + ")</td>"
					+ "<td style='max-width: 4em'>" + projectSummary.for_percentage_3 + "&nbsp;%&nbsp;</td>"
					+ "</tr>";
				}
				forDistributionTable += "</table>";
				return forDistributionTable;
			}
			return projectSummary[row]; 
		});

}

//==== Pie Chart for Instance and Core Quota.

// Pie chart constants.

var PIE_CHART_WIDTH = 92;
var PIE_CHART_HEIGHT = 92;
var PIE_CHART_RADIUS = Math.min(PIE_CHART_WIDTH, PIE_CHART_HEIGHT) / 2;
var PIE_CHART_INNER_RADIUS = PIE_CHART_RADIUS*0.0;

function graphQuota(pageAreaSelector, quotaKey, usage) {
		
	var color = d3.scale.ordinal()
				// Color for used quota then unused quota.
				.domain("0", "1")
			    .range(["#006ccf", "#f2f2f2"]);

	var pie = d3.layout.pie()
				.value(function(d) { 
						return d; 
				});

	var arc = d3.svg.arc()
				.outerRadius(PIE_CHART_RADIUS)
				.innerRadius(PIE_CHART_INNER_RADIUS)
				.startAngle(function(d) { return 2*Math.PI - d.startAngle; })
				.endAngle(function(d) { return 2*Math.PI - d.endAngle; });

	var svg = d3.select(pageAreaSelector).append("svg")
				.attr("width", PIE_CHART_WIDTH)
				.attr("height", PIE_CHART_HEIGHT)
				.append("g")
					.attr("transform", "translate(" + PIE_CHART_WIDTH / 2 + "," + PIE_CHART_HEIGHT / 2 + ")");

	var g = svg.selectAll(".arc")
				.data(pie(usage))
				.enter().append("g")
				.attr("class", "arc");
		
	g.append("path")
				.attr("d", arc)
				.style("fill", function(d, i) { 
					return color(i); 
				});

	g.append("text")
				.attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
				.attr("dy", ".35em")
				.style("text-anchor", "middle")
				.style("font-weight", "bold")
				.style("font-family", "'Helvetica Neue', Helvetica, Arial, sans-serif")
				.style("font-size", "13px")
				.text(function(d) { 
					var usageQuota = (usage[0] + usage[1]) + "";
					return d.data == "0" ? "" : d.data + "/" + usageQuota; 
				});
}

//==== Project Allocation: Assembling the Pieces.
// Table and 3 pie charts.

function projectDetails() {
	d3.json("/nacc/rest/for_codes", function(error, forTranslation) {
		d3.json("/nacc/rest/allocations/" + allocationId + "/project/summary", function(error, projectSummary) {
			tabulateSummary("#project-summary", projectSummary, forTranslation);
			var coreUsage = [projectSummary.cores, projectSummary.core_quota - projectSummary.cores];
			graphQuota("#core-pie-chart","cores", coreUsage);
			instanceUsage = [projectSummary.instances, projectSummary.instance_quota - projectSummary.instances];
			graphQuota("#instance-pie-chart","instances", instanceUsage);
		});
	});
}

projectDetails();
