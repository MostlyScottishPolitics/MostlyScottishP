$(function () {
    var w=960, h=750;
var pLoad = [];
var party={};

var border = .5;
var bordercolor = "black";

var gssCode = {
    "S12000005":"Mid Scotland and Fife",
    "S12000014":"Central Scotland",
    "S12000030":"Mid Scotland and Fife",
    "S12000006":"South Scotland",
    "S12000008":"South Scotland",
    "S12000011":"West Scotland",
    "S12000018":"West Scotland",
    "S12000021":"West Scotland",
    "S12000028":"South Scotland",
    "S12000029":"South Scotland",
    "S12000035":"Highlands and Islands",
    "S12000038":"West Scotland",
    "S12000039":"West Scotland",
    "S12000044":"Central Scotland",
    "S12000045":"West Scotland",
    "S12000046":"Glasgow",
    "S12000010":"South Scotland",
    "S12000019":"Lothian",
    "S12000026":"South Scotland",
    "S12000036":"Lothian",
    "S12000040":"Lothian",
    "S12000013":"Highlands and Islands",
    "S12000017":"Highlands and Islands",
    "S12000023":"Highlands and Islands",
    "S12000027":"Highlands and Islands",
    "S12000015":"Mid Scotland and Fife",
    "S12000020":"Highlands and Islands",
    "S12000033":"North East Scotland",
    "S12000034":"North East Scotland",
    "S12000024":"Mid Scotland and Fife",
    "S12000041":"North East Scotland",
    "S12000042":"North East Scotland"
};

var color = {
    "Central Scotland" : "#0065BD",
    "South Scotland" : "#70193d",
    "North East Scotland" : "#002549",
    "Lothian" : "#F000",
    "Highlands and Islands" : "#59118e",
    "Glasgow" : "#d10056",
    "Mid Scotland and Fife" : "#b58c0a",
    "West Scotland" : "#3d8e33"
};

/*var colors = [["Scottish Conservative and Unionist Party","#5ABFF4"],
			["Scottish Labour","#EB2743"],
			["Scottish Liberal Democrats","#FF784E"],
			["Scottish National Party","#F6DC60"],
			["Scottish Green Party","#31C48E"],
			["Independent","#986561"],
			["No Party Affiliation", "#475070"]]
			;*/

var projection = d3.geo.albers()
    .center([0, 55.4])
    .rotate([4.4, 0])
    .parallels([50, 60])
    .scale(9000)
    .translate([w/2, h/1.2]);

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select(".map")
    .append("svg")
    .attr("width",w)
    .attr("height",h)
    .style("background","#fff");
    
var borderPath = svg.append("rect")
       			.attr("x", 0)
       			.attr("y", 0)
       			.attr("height", h)
       			.attr("width", w)
       			.style("stroke", bordercolor)
       			.style("fill", "none")
       			.style("stroke-width", border);

var generateVisualization = function()
{
d3.json("/static/json/scotland-topojson-file.json",function(err,load){
    svg.selectAll("path")
        .data(topojson.feature(load,load.objects.layer1).features)
      .enter().append("path")
        .attr("d",path)
        .style("fill",function(d){return color[gssCode[d.properties.gss]];})
        .style("opacity", 0.6)
        .style("stroke", "#fff")
      	.append("title")
        .text(function(d){return gssCode[d.properties.gss]+"\n"+party[gssCode[d.properties.gss]];});
});

/*var legend = svg.selectAll(".legend")
      			.data(colors)
    			.enter().append("g")
      			.attr("class", "legend")
      			.attr("transform", function(d, i) { return "translate(0," + (i+1) * 20 + ")"; });

  				legend.append("rect")
      			.attr("x", w - 285)
     			.attr("width", 15)
      			.attr("height", 15)
     			.style("fill", function(d){return d[1]})
     			.style("opacity", .7);

 				 legend.append("text")
      				.attr("x", w - 268)
      				.attr("y", 12)
      				.attr("class", "text")
    				.text(function(d) { return d[0]; });*/
};
d3.csv("/static/csv/map_data.csv", function(error, d) {
  				pLoad = d.map(function(d) { return [d["region"], d["party"]]; 
  				});
  				
  				for (i = 0; i < 8; i++) { 
    			party[pLoad[i][0]] = pLoad[i][1];
				}
  				generateVisualization();});
    })