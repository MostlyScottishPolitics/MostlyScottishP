var scatter = function (dataList) {
//setting up variables
	var w = 800;
	var h = 400;
	var padding = 20;
	var border = 1;
	var bordercolor = "black";
	var dataset = dataList;//Hold the data loaded from csv file
	//setting a color for each party
	var colors_array = [];
	//colors dictionary
	var colors = {};

			//Create SVG element
			var svg = d3.select("#plot")
						.append("svg")
						.attr("width", w)
						.attr("height", h);

			//Create border for the svg element
			var borderPath = svg.append("rect")
       			.attr("x", 0)
       			.attr("y", 0)
       			.attr("height", h)
       			.attr("width", w)
       			.style("stroke", bordercolor)
       			.style("fill", "none")
       			.style("stroke-width", border);

			// add the tooltip area to the webpage
			var tooltip = d3.select("#plot").append("div")
    		.attr("class", "tooltip")
   		 	.style("opacity", 0);

		var generateVisualization = function(){
			console.log("HERE!!!!!!!!");
			//Create scaling functions
				
			// X scaling functions
			var xScale = d3.scale.linear()
								 .domain([d3.min(dataset, function(d) { return d[0]; }), d3.max(dataset, function(d) { return d[0]; })])
								 .rangeRound([padding, w - padding * 10]);
			// Y scaling functions
			var yScale = d3.scale.linear()
								 .domain([d3.min(dataset, function(d) { return d[1]; }), d3.max(dataset, function(d) { return d[1]; })])
								 .rangeRound([h - padding, padding]);


							  
			//Create circles
				svg.append("g")
			   .attr("id", "circles")
			   .selectAll("circle")
			   .data(dataset)
			   .enter()
			   .append("circle")
			   .attr("class", "dot")
			   .attr("cx", function(d) {
					return xScale(d[0]);
			   })
			   .attr("cy", function(d) {
					return yScale(d[1]);
			   })
			   .attr("r", 8)
			   .style("fill", function(d){
				return colors[d[2]];
			   })
			   .style("opacity", .5)
			   .on("click", function(d) {
          		tooltip.transition()
               .duration(200)
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 5) + "px")
               .style("opacity", .9);
				tooltip.text(d[3]);
               })
				.on("mouseout", function(d) {
          		tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      			});

			//Create legend
				var legend = svg.selectAll(".legend")
      			.data(colors_array)
    			.enter().append("g")
      			.attr("class", "legend")
      			.attr("transform", function(d, i) { return "translate(0," + (i+1) * 20 + ")"; });
			//legend colors
  				legend.append("rect")
      			.attr("x", w - 188)
     			.attr("width", 15)
      			.attr("height", 15)
     			.style("fill", function(d){return d[1]})
     			.style("opacity", .5);
			//legend text
 				 legend.append("text")
      				.attr("x", w - 171)
      				.attr("y", 12)
      				.attr("class", "text")
    				.text(function(d) { return d[0]; });
    				
    			// Scale Changes as we zoom
    			svg.call(d3.behavior.zoom().x(xScale).y(yScale).on("zoom", zoom));  // Call funtion zoom

   		 		// Zoom into data (.dot)
    			function zoom() {
        			svg.selectAll(".dot")
            			 .attr("cx", function(d) { return xScale(d[0]); })
           				 .attr("cy", function(d) { return yScale(d[1]); });
    }

			};


			//Load the data from the csv files
			d3.csv("/static/csv/parties_colors.csv", function(error, d) {
  				colors_array = d.map(function(d) { return [d["Party"], d["Color"]];
  				});
				for(var i = 0; i < colors_array.length; i++){
					colors[colors_array[i][0]] = colors_array[i][1];
				}
				generateVisualization();
  				});

}

var reset = function(dataList) {
	$('#plot').empty();
	scatter(dataList)
};

/*// get me the cookie

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$('#submitForm').click(function(event) {
	event.preventDefault();
    var str = $('#post-form').serialize();
    $('#paramsSent').html(str);

    $.post('',
          str,
          function(data){
			  	reset("OutputMatrix.csv");

          });
 });
//Reset the visualization to its original state

$('#reset').click(function() {
	event.preventDefault();
    $.get('',
          function(data){

			$('input[name=party]').attr('checked', false);
			$('input[name=topic]').attr('checked', false);
			  	reset("OutputMatrix.csv");

          });
	$.ajax({
        url : '',
        type : "POST",
        data : {
			csrfmiddlewaretoken: csrftoken
		},

		success : function(json) {
			$('input[name=party]').attr('checked', false);
			$('input[name=topic]').attr('checked', false);
			reset("OutputMatrix.csv");
    		console.log("success"); // another sanity check
},

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
 });
*/
