////// FOR Table for NeCTAR Allocations

//==== FOR Table

var headings = {
	"for_code" : "Code",
	"for_name" : "Name",
	"percent" : "%",
	"count" : "Count",
};

//==== HTML Table For Allocations for FOR Codes.
// Populated on page load. Dynamic update after page load is not supported.

function buildTable(pageAreaSelector, isCoreQuota) {
	// Define the table with heading.
	var table = d3.select(pageAreaSelector).append("table")
					.attr("class", "table-striped table-bordered table-condensed");	
	var thead = table.append("thead");
	var tbody = table.append("tbody");
	
	// The row headers
	var headerRow = thead.append("tr");
	headerRow.append("th")
		.attr("class", "col0")
		.style("min-width", "20px")
		.text(headings["for_code"]);
	headerRow.append("th")
		.attr("class", "col1")
		.style("min-width", "20px")
		.text(headings["for_name"]);
	headerRow.append("th")
		.attr("class", "col2")
		.style("min-width", "20px")
		.text(headings["percent"]);
	headerRow.append("th")
		.attr("class", "col3")
		.style("min-width", "20px")
		.text(isCoreQuota ? "Cores" : "Instances");
	headerRow.append("th")
		.attr("class", "col4")
		.text("Zoom");
	
	return table;
}

function tabulateAllocations(table, dataset, total, isCoreQuota) {
	
	dataset.sort(function(a, b){return b.value - a.value; });

	// Adjust the header
	
	var thead = table.select("thead");
	
	thead.select("th.col3")
		.text(function(row) { 
				return isCoreQuota ? "Cores" : "Instances"; 
			});

	// Attach the data
	
	var tbody = table.select("tbody");
	var rows = tbody.selectAll("tr").data(dataset);

	// Update the existing data records

	rows.select("td.col0")
		.style("background-color", function (d, i) {
				return paletteStack.tos()(d.colourIndex);
		})
		.text(function(row) { 
				return row["target"]; 
			});
	
	rows.select("td.col1")
		.text(function(row) { 
				var forCode = row["target"];
				return forTitleMap[forCode].toLowerCase(); 
			});
	
	rows.select("td.col2")
		.text(function(row) { 
				var percent = row["value"] * 100.00 / total;
				return percent.toFixed(2); 
			});
	
	rows.select("td.col3")
		.text(function(row) { 
			// Round up.
				var value = row["value"];
				var roundedValue = Math.round(value);
				if ((value - roundedValue) > 0) {
					roundedValue += 1;
				}
				return roundedValue; 
			});		
	
	rows.select("td.col4");		

	// Add new data records

	var newRows = rows.enter().append("tr");
	newRows.attr('data-row',function(d,i){return i; });

	newRows.append("td")
		.attr("class", "col0")
		.style("min-width", "20px")
		.style("background-color", function (d, i) {
				return paletteStack.tos()(d.colourIndex);
		})
		.style("color", "white")
		.text(function(row) { 
				return row["target"]; 
			});
	
	newRows.append("td")
		.attr("class", "col1")
		.style("min-width", "20px")
		.style("text-align", "left")
		.style("text-transform", "capitalize")
		.text(function(row) { 
				var forCode = row["target"];
				return forTitleMap[forCode].toLowerCase(); 
			});
	
	newRows.append("td")
		.attr("class", "col2")
		.style("min-width", "20px")
		.style("text-align", "right")
		.text(function(row) { 
				var percent = row["value"] * 100.00 / total;
				return percent.toFixed(2); 
			});

	newRows.append("td")
		.attr("class", "col3")
		.style("min-width", "20px")
		.style("text-align", "right")
		.text(function(row) { 
			// Round up.
				var value = row["value"];
				var roundedValue = Math.round(value);
				if ((value - roundedValue) > 0) {
					roundedValue += 1;
				}
				return roundedValue; 
			});		

	newRows.append("td")
		.attr("class", "col4")
		.style("text-align", "center")
		.style("cursor", "pointer")
		.on("click", zoomIn)
		.html("<span class='glyphicon glyphicon-zoom-in'></span>");		

	// Remove old records.
	
	var oldRows = rows.exit();
	var oldCells = oldRows.selectAll("td");
	oldCells.remove();
	oldRows.remove();
	
	var containerHeight = $("#table-area").height() + RADIUS * 2;
	$("#inner-plot-container, #outer-plot-container").height(containerHeight);
	$(document.body).trigger("sticky_kit:recalc");
}

var table = buildTable("#table-area");



