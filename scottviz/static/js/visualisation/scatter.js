//Width and height
var w = 800;
var h = 400;
var padding = 20;
var border = 1;
var bordercolor = "black";
var dataset = [];
var colors = [
        ["Scottish Conservative and Unionist Party", "#5ABFF4"],
        ["Scottish Labour", "#846DD4"],
        ["Scottish Liberal Democrats", "#FA6485"],
        ["Scottish National Party", "#F6DC60"],
        ["Scottish Green Party", "#31C48E"],
        ["Independent", "#986561"],
        ["No Party Affiliation", "#475070"]
    ]
    ;

//Create SVG element
var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

var borderPath = svg.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("height", h)
    .attr("width", w)
    .style("stroke", bordercolor)
    .style("fill", "none")
    .style("stroke-width", border);

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var generateVisualization = function () {
    //Create scaling functions

    // X scaling functions
    var xScale = d3.scale.linear()
        .domain([d3.min(dataset, function (d) {
            return d[0];
        }), d3.max(dataset, function (d) {
            return d[0];
        })])
        .rangeRound([padding, w - padding * 10]);
    // Y scaling functions
    var yScale = d3.scale.linear()
        .domain([d3.min(dataset, function (d) {
            return d[1];
        }), d3.max(dataset, function (d) {
            return d[1];
        })])
        .rangeRound([h - padding, padding]);

    //Define X axis
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .tickFormat("");

    //Define Y axis
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .tickFormat("");

    //Create circles
    svg.append("g")
        .attr("id", "circles")
        .selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("cx", function (d) {
            return xScale(d[0]);
        })
        .attr("cy", function (d) {
            return yScale(d[1]);
        })
        .attr("r", 8)
        .style("fill", function (d) {
            if (d[2] == "Scottish Conservative and Unionist Party")
                return "#5ABFF4";
            if (d[2] == "Scottish Labour")
                return "#846DD4";
            if (d[2] == "Scottish Liberal Democrats")
                return "#FA6485";
            if (d[2] == "Scottish National Party")
                return "#F6DC60";
            if (d[2] == "Scottish Green Party")
                return "#31C48E";
            if (d[2] == "Independent")
                return "#986561";
            if (d[2] == "No Party Affiliation")
                return "#475070";
        })
        .style("opacity", .5)
        .on("mouseover", function (d) {
            tooltip.transition()
                .duration(200)
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 5) + "px")
                .style("opacity", .9);
            tooltip.text(d[3]);
        })
        .on("mouseout", function (d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        });

    var legend = svg.selectAll(".legend")
        .data(colors)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
            return "translate(0," + (i + 1) * 20 + ")";
        });

    legend.append("rect")
        .attr("x", w - 188)
        .attr("width", 15)
        .attr("height", 15)
        .style("fill", function (d) {
            return d[1]
        })
        .style("opacity", .5);

    legend.append("text")
        .attr("x", w - 171)
        .attr("y", 12)
        .attr("class", "text")
        .text(function (d) {
            return d[0];
        });

    // Scale Changes as we zoom
    svg.call(d3.behavior.zoom().x(xScale).y(yScale).on("zoom", zoom));  // Call funtion zoom

    // Zoom into data (.dot)
    function zoom() {
        svg.selectAll(".dot")
            .attr("cx", function (d) {
                return xScale(d[0]);
            })
            .attr("cy", function (d) {
                return yScale(d[1]);
            });
        d3.select('.x.axis').call(xAxis);
        d3.select('.y.axis').call(yAxis);
    }

};

d3.csv("{{PROJECT_PATH}}/NewPCA/OutputMatrix.csv", function (error, d) {
    dataset = d.map(function (d) {
        return [ +d["X"], +d["Y"], d["Party"], d["MSP Name"]];
    });
    generateVisualization();
});