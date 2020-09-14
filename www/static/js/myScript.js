var moviesData=[
				{
                        genre : "Action",
                        value : 6484
                },
                {
                        genre : "Adventure",
                        value : 3345
                },
                {
                        genre : "Animation",
                        value : 1913
                },
                {
                        genre : "Comedy",
                        value : 12990
                },
                {
                        genre : "Crime",
                        value : 3964
                },
                {
                        genre : "Documentary",
                        value : 3920
                },
                {
                        genre : "Drama",
                        value : 19930
                },
                {
                        genre : "Family",
                        value : 2389
                },
                {
                        genre : "Fantasy",
                        value : 2006
                },
                {
                        genre : "Foreign",
                        value : 1307
                },
                {
                        genre : "History",
                        value : 1267
                },
                {
                        genre : "Horror",
                        value : 4530
                },
                {
                        genre : "Music",
                        value : 1497
                },
                {
                        genre : "Mystery",
                        value : 2098
                },
                {
                        genre : "Romance",
                        value : 6092
                },
                {
                        genre : "Science Fiction",
                        value : 2516
                },
                {
                        genre : "TV Movie",
                        value : 672
                },
                {
                        genre : "Thriller",
                        value : 6420
                },
                {
                        genre : "War",
                        value : 1135
                },
                {
                        genre : "Western",
                        value : 923
                }
];


var svg=d3.select("#svg");

var padding={top:20,right:30, bottom:30,left:50};
var colors=d3.schemeCategory20b;
var chartArea={
		"width":parseInt(svg.style("width"))-padding.left-padding.right,
		"height":parseInt(svg.style("height"))-padding.top-padding.bottom,

};

var yScale = d3.scaleLinear()
	.domain([0,d3.max(moviesData,function (d,i) {return d.value})])
	.range([chartArea.height,0]).nice();

var xScale = d3.scaleBand()
	.domain(moviesData.map(function(d){return d.genre}))
	.range([0,chartArea.width])
	.padding(.2);


var xAxis=svg.append("g")
	.classed("xAxis",true)
	.attr(
		'transform','translate('+padding.left+','+(chartArea.height+ padding.top)+')'
		)
	.call(d3.axisBottom(xScale));

var yAxisFn=d3.axisLeft(yScale);
var yAxis=svg.append("g")
	.classed("yAxis",true)
	.attr(
		'transform','translate('+padding.left+','+padding.top+')'
		);
yAxisFn(yAxis);


var grid=svg.append("g")
	.attr("class","grid")
	.attr(
		'transform','translate('+padding.left+','+padding.top+')'
		)
	.call(d3.axisLeft(yScale)
		.tickSize(-(chartArea.width))
		.tickFormat("")
		);



var rectGrp=svg.append("g").attr('transform','translate('+padding.left+','+padding.top+')'
	);

rectGrp.selectAll("rect").data(moviesData).enter()
	.append("rect")
	.attr("width",xScale.bandwidth())
	.attr("height", function (d,i) {
		return chartArea.height-yScale(d.value);
	})
	.attr("x",function (d,i){
		return xScale(d.genre);
	})
	.attr("y",function (d,i){
		return yScale(d.value);
	})
	.attr("fill",function (d){
		return "#483D8B";
	});
