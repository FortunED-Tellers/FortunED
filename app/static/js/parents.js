// build chart
var svgWidth = 1125
var svgHeight = 500

var margin = {
  top: 20,
  right: 40,
  bottom: 60,
  left: 60
}

var width = svgWidth - margin.left - margin.right
var height = svgHeight - margin.top - margin.bottom

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select("#scatter")
  .append("svg")
  .attr("height", svgHeight)
  .attr("width", svgWidth)

var tooltip = d3.select("body").append("div").attr("class", "toolTip");

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`)

// Add X axis
var x = d3.scaleBand()
  .range([0, width])
  .padding([0.2])

var xAxis = chartGroup.append("g")
  .attr("transform", "translate(0," + height + ")")

// Add Y axis
var y = d3.scaleLinear()
  .range([ height, 0 ]);

var yAxis = chartGroup.append("g")

function update(label){
  d3.csv("/static/data/processed/gender_race_employment.csv").then(function(data) {
    data.forEach(function(item){
      item.Employed = +item.Employed
      item.Unemployed = +item.Unemployed
    })

    var total = []
    var men = []
    var women = []
    var white = []
    var black = []
    var asian = []
    var hispanic = []

    for (var i=0; i<data.length; i++){
      if (data[i].Category.startsWith("Total")){
        total.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Category.startsWith("Men")){
        men.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Category.startsWith("Women")){
        women.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Category.startsWith("White")){
        white.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Category.startsWith("Black")){
        black.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Category.startsWith("Asian")){
        asian.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Category.startsWith("Hispanic")){
        hispanic.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
    }

    var table = []

    if (label === "total"){
      table = total
    }
    else if (label === "men"){
      table = men
    }
    else if (label === "women"){
      table = women
    }
    else if (label === "white"){
      table = white
    }
    else if (label === "black"){
      table = black
    }
    else if (label === "asian"){
      table = asian
    }
    else if (label === "hispanic"){
      table = hispanic
    }

    var subgroups = ["Employed", "Unemployed"]

    x.domain(table.map(function(d) { return d.degree }))
    xAxis.transition().duration(100).call(d3.axisBottom(x).tickSize(0))

    y.domain([0, 100]);
    yAxis.transition().duration(100).call(d3.axisLeft(y))
      
    // Another scale for subgroup position?
    var xSubgroup = d3.scaleBand()
      .domain(subgroups)
      .range([0, x.bandwidth()])
      .padding([0.05])
  
    // color palette = one color per subgroup
    var color = d3.scaleOrdinal()
      .domain(subgroups)
      .range(['#9DC183','#ED2939'])
    
    chartGroup.select(".bars").remove()
    chartGroup.selectAll(".aText").remove()

    // variable u: map data to existing bars
    var u = chartGroup.append("g")
      .classed("bars", true)
      .selectAll("g")
      .data(table)
    
    // Show the bars
    u.enter()
    .merge(u)
    .append("g")
      .attr("transform", function(d)  { return "translate(" + x(d.degree) + ",0)"; })
    .selectAll("rect")
    .data(function(d) { return subgroups.map(function(key) { return {key: key, value: d[key]} }) })
    .enter()
    .append("rect")
      .attr("x", function(d) { return xSubgroup(d.key); })
      .attr("y", function(d) { return y(d.value); })
      .attr("width", xSubgroup.bandwidth())
      .attr("height", function(d) { return height - y(d.value); })
      .attr("fill", function(d) { return color(d.key); })
    .on("mouseover", function(d){
      tooltip
        .style("left", d3.event.pageX - 50 + "px")
        .style("top", d3.event.pageY - 70 + "px")
        .style("display", "inline-block")
        .html((d.key) + "<br>" + (d.value) + "%")
      })
    .on("mouseout", function(d){ tooltip.style("display", "none")})

    // Create axes labels
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 10)
      .attr("x", 0 - (height-125))
      .attr("dy", "1em")
      .attr("class", "aText")
      .text("Percent of the Population")

    chartGroup.append("text")
      .attr("transform", `translate(${width/2-100}, ${height + margin.top + 10})`)
      .attr("class", "aText")
      .text("Educational Attainment")
      var title = ""

      if (label === "total") {
        title = "Overall"
      }
      else if (label === "men") {
        title  = "Men"
      }
      else if (label === "women") {
        title  = "Women"
      }
      else if (label === "white") {
        title  = "White"
      }
      else if (label === "black") {
        title  = "Black"
      }
      else if (label === "asian") {
        title  = "Asian"
      }
      else if (label === "hispanic") {
        title  = "Hispanic"
      }
      
      chartGroup.append("text")
      .attr("x", (width / 2))             
      .attr("y", "5")
      .attr("class", "aText")
      .style("font-size", "20px") 
      .text(title);
      })
  }
  
update("total")