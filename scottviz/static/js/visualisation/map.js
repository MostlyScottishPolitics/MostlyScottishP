$(function () {
        $.support.cors = true;

//setting up variables
var w=960, h=750;
var pLoad = [];
var parties={};//hold parties for each region
var border = .5;
var bordercolor = "black";
var ids = {};//hold id for each region

//link each council area to the region it belongs to
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

//hold the color for each region
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
//The projection of the map
var projection = d3.geo.albers()
    .center([0, 55.4])
    .rotate([4.4, 0])
    .parallels([50, 60])
    .scale(9000)
    .translate([w/2, h/1.2]);
//path that create the map
var path = d3.geo.path()
    .projection(projection);
//Create svg element
var svg = d3.select(".map")
    .append("svg")
    .attr("width",w)
    .attr("height",h)
    .style("background","#fff");
//Create border for svg
var borderPath = svg.append("rect")
       			.attr("x", 0)
       			.attr("y", 0)
       			.attr("height", h)
       			.attr("width", w)
       			.style("stroke", bordercolor)
       			.style("fill", "none")
       			.style("stroke-width", border);

//the function that create the visualization
var generateVisualization = function()
{
//load the topojson file
d3.json("/static/json/scotland-topojson-file.json",function(err,load){
    svg.selectAll("path")
        .data(topojson.feature(load,load.objects.layer1).features)
      .enter().append("path")
        .attr("d",path)
        .style("fill",function(d){return color[gssCode[d.properties.gss]];})
        .style("opacity", 0.6)
        .style("stroke", "#fff")
        .on("click", function(d){
        location.href='/constituency/'+ids[gssCode[d.properties.gss]]+'/';})
      	.append("title")
        .text(function(d){
        var str = gssCode[d.properties.gss];
		var object = parties[gssCode[d.properties.gss]];
		if(object["Scottish National Party"] > 0)
			str = str+"\n"+"Scottish National Party: "+object["Scottish National Party"];
		if(object["Scottish Labour"] > 0)
			str = str+"\n"+"Scottish Labour: "+object["Scottish Labour"];
		if(object["Scottish Conservative and Unionist Party"] > 0)
			str = str+"\n"+"Scottish Conservative and Unionist Party: "+object["Scottish Conservative and Unionist Party"];
		if(object["Independent"] > 0)
			str = str+"\n"+"Independent: "+object["Independent"];
		if(object["Scottish Green Party"] > 0)
			str = str+"\n"+"Scottish Green Party: "+object["Scottish Green Party"];
		if(object["Scottish Liberal Democrats"] > 0)
			str = str+"\n"+"Scottish Liberal Democrats: "+object["Scottish Liberal Democrats"];
		if(object["No Party Affiliation"] > 0)
			str = str+"\n"+"No Party Affiliation: "+object["No Party Affiliation"];
		return str;
        });
});
};
//Load csv file of regions and the parties distribution
d3.csv("/static/csv/map_data.csv", function(error, d) {
  				pLoad = d.map(function(d) { return [d["Region"],+d["id"], +d["Scottish National Party"],+d["Scottish Labour"],+d["Scottish Conservative and Unionist Party"],+d["Independent"],+d["Scottish Green Party"],+d["Scottish Liberal Democrats"],+d["No Party Affiliation"]];
  				});

  				for (i = 0; i < 8; i++) {
    			parties[pLoad[i][0]] = {"Scottish National Party": pLoad[i][2], "Scottish Labour": pLoad[i][3], "Scottish Conservative and Unionist Party": pLoad[i][4], "Independent": pLoad[i][5], "Scottish Green Party": pLoad[i][6], "Scottish Liberal Democrats": pLoad[i][7], "No Party Affiliation": pLoad[i][8]};
                ids[""+pLoad[i][0]] = pLoad[i][1];
				}
  				generateVisualization();});
    })
