$(function () {
    var w = 960, h = 750;
    var pLoad = [];
    var party = {};

    var border = .5;
    var bordercolor = "black";

    var gssCode = {
        "S12000005": "Central",
        "S12000014": "Central",
        "S12000030": "Central",
        "S12000006": "Dumfries and Galloway",
        "S12000008": "Strathclyde",
        "S12000011": "Strathclyde",
        "S12000018": "Strathclyde",
        "S12000021": "Strathclyde",
        "S12000028": "Strathclyde",
        "S12000029": "Strathclyde",
        "S12000035": "Strathclyde",
        "S12000038": "Strathclyde",
        "S12000039": "Strathclyde",
        "S12000044": "Strathclyde",
        "S12000045": "Strathclyde",
        "S12000046": "Strathclyde",
        "S12000010": "Lothian",
        "S12000019": "Lothian",
        "S12000026": "Lothian",
        "S12000036": "Lothian",
        "S12000040": "Lothian",
        "S12000013": "Highland",
        "S12000017": "Highland",
        "S12000023": "Highland",
        "S12000027": "Highland",
        "S12000015": "Fife",
        "S12000020": "Grampian",
        "S12000033": "Grampian",
        "S12000034": "Grampian",
        "S12000024": "Tayside",
        "S12000041": "Tayside",
        "S12000042": "Tayside"
    };


var color = {
    "Scottish Conservative and Unionist Party": "#5ABFF4",
    "Scottish Labour": "#846DD4",
    "Scottish Liberal Democrats": "#FA6485",
    "Scottish National Party": "#F6DC60",
    "Scottish Green Party": "#31C48E",
    "Independent": "#986561",
    "No Party Affiliation": "#475070"
};

var colors = [["Scottish Conservative and Unionist Party", "#5ABFF4"],
        ["Scottish Labour", "#846DD4"],
        ["Scottish Liberal Democrats", "#FA6485"],
        ["Scottish National Party", "#F6DC60"],
        ["Scottish Green Party", "#31C48E"],
        ["Independent", "#986561"],
        ["No Party Affiliation", "#475070"]]
    ;

var projection = d3.geo.albers()
    .center([0, 55.4])
    .rotate([4.4, 0])
    .parallels([50, 60])
    .scale(9000)
    .translate([w / 2, h / 1.2]);

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select(".map")
    .append("svg")
    .attr("width", w)
    .attr("height", h)
    .style("background", "#fff");

var borderPath = svg.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("height", h)
    .attr("width", w)
    .style("stroke", bordercolor)
    .style("fill", "none")
    .style("stroke-width", border);

var generateVisualization = function () {
    d3.json("/static/json/scotland-topojson-file.json", function (err, load) {
        svg.selectAll("path")
            .data(topojson.feature(load, load.objects.layer1).features)
            .enter().append("path")
            .attr("d", path)
            .style("fill", function (d) {
                return color[party[gssCode[d.properties.gss]]];
            })
            .style("opacity", 0.7)
            .style("stroke", "#fff")
            .append("title")
            .text(function (d) {
                return gssCode[d.properties.gss];
            });
    });

    var legend = svg.selectAll(".legend")
        .data(colors)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
            return "translate(0," + (i + 1) * 20 + ")";
        });

    legend.append("rect")
        .attr("x", w - 285)
        .attr("width", 15)
        .attr("height", 15)
        .style("fill", function (d) {
            return d[1]
        })
        .style("opacity", .7);

    legend.append("text")
        .attr("x", w - 268)
        .attr("y", 12)
        .attr("class", "text")
        .text(function (d) {
            return d[0];
        });
};
d3.csv("/static/csv/map_data.csv", function (error, d) {
    pLoad = d.map(function (d) {
        return [d["region"], d["party"]];
    });

    for (i = 0; i < 8; i++) {
        party[pLoad[i][0]] = pLoad[i][1];
    }
    generateVisualization();
});
    })