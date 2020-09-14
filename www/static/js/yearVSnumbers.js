var yearCount=[
{ year : 1914, value : 19 },
{ year : 1915, value : 29 },
{ year : 1916, value : 32 },
{ year : 1917, value : 17 },
{ year : 1918, value : 16 },
{ year : 1919, value : 23 },
{ year : 1920, value : 29 },
{ year : 1921, value : 33 },
{ year : 1922, value : 34 },
{ year : 1923, value : 23 },
{ year : 1924, value : 39 },
{ year : 1925, value : 40 },
{ year : 1926, value : 50 },
{ year : 1927, value : 41 },
{ year : 1928, value : 66 },
{ year : 1929, value : 76 },
{ year : 1930, value : 81 },
{ year : 1931, value : 99 },
{ year : 1932, value : 135 },
{ year : 1933, value : 147 },
{ year : 1934, value : 141 },
{ year : 1935, value : 144 },
{ year : 1936, value : 152 },
{ year : 1937, value : 155 },
{ year : 1938, value : 127 },
{ year : 1939, value : 134 },
{ year : 1940, value : 152 },
{ year : 1941, value : 147 },
{ year : 1942, value : 146 },
{ year : 1943, value : 144 },
{ year : 1944, value : 142 },
{ year : 1945, value : 147 },
{ year : 1946, value : 128 },
{ year : 1947, value : 156 },
{ year : 1948, value : 157 },
{ year : 1949, value : 174 },
{ year : 1950, value : 184 },
{ year : 1951, value : 196 },
{ year : 1952, value : 194 },
{ year : 1953, value : 199 },
{ year : 1954, value : 191 },
{ year : 1955, value : 209 },
{ year : 1956, value : 218 },
{ year : 1957, value : 244 },
{ year : 1958, value : 220 },
{ year : 1959, value : 224 },
{ year : 1960, value : 218 },
{ year : 1961, value : 203 },
{ year : 1962, value : 229 },
{ year : 1963, value : 233 },
{ year : 1964, value : 254 },
{ year : 1965, value : 247 },
{ year : 1966, value : 306 },
{ year : 1967, value : 288 },
{ year : 1968, value : 338 },
{ year : 1969, value : 305 },
{ year : 1970, value : 351 },
{ year : 1971, value : 377 },
{ year : 1972, value : 381 },
{ year : 1973, value : 356 },
{ year : 1974, value : 348 },
{ year : 1975, value : 332 },
{ year : 1976, value : 333 },
{ year : 1977, value : 334 },
{ year : 1978, value : 321 },
{ year : 1979, value : 338 },
{ year : 1980, value : 360 },
{ year : 1981, value : 359 },
{ year : 1982, value : 368 },
{ year : 1983, value : 352 },
{ year : 1984, value : 362 },
{ year : 1985, value : 368 },
{ year : 1986, value : 391 },
{ year : 1987, value : 462 },
{ year : 1988, value : 467 },
{ year : 1989, value : 439 },
{ year : 1990, value : 426 },
{ year : 1991, value : 426 },
{ year : 1992, value : 453 },
{ year : 1993, value : 489 },
{ year : 1994, value : 544 },
{ year : 1995, value : 600 },
{ year : 1996, value : 633 },
{ year : 1997, value : 661 },
{ year : 1998, value : 722 },
{ year : 1999, value : 723 },
{ year : 2000, value : 788 },
{ year : 2001, value : 863 },
{ year : 2002, value : 903 },
{ year : 2003, value : 882 },
{ year : 2004, value : 992 },
{ year : 2005, value : 1124 },
{ year : 2006, value : 1269 },
{ year : 2007, value : 1319 },
{ year : 2008, value : 1470 },
{ year : 2009, value : 1585 },
{ year : 2010, value : 1501 },
{ year : 2011, value : 1666 },
{ year : 2012, value : 1721 },
{ year : 2013, value : 1887 },
{ year : 2014, value : 1973 },
{ year : 2015, value : 1904 },
{ year : 2016, value : 1604 },
{ year : 2017, value : 531 },
{ year : 2018, value : 5 },
{ year : 2020, value : 88 }
]


var svg=d3.select("#svg3");

var padding={top:20,right:30, bottom:30,left:40};
var colors=d3.schemeCategory20b;
var chartArea={
		"width":parseInt(svg.style("width"))-padding.left-padding.right,
		"height":parseInt(svg.style("height"))-padding.top-padding.bottom,

};

var yScale = d3.scaleLinear()
	.domain([0,d3.max(yearCount,function (d,i) {return d.value})])
	.range([chartArea.height,0]).nice();

var xScale = d3.scaleBand()
	.domain(yearCount.map(function(d){return d.year}))
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

rectGrp.selectAll("rect").data(yearCount).enter()
	.append("rect")
	.attr("width",xScale.bandwidth())
	.attr("height", function (d,i) {
		return chartArea.height-yScale(d.value);
	})
	.attr("x",function (d,i){
		return xScale(d.year);
	})
	.attr("y",function (d,i){
		return yScale(d.value);
	})
	.attr("fill",function (d,i){
		return colors[i];
	});
