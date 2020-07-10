// build chart
var svgWidth = 960
var svgHeight = 500

var margin = {
  top: 30,
  right: 30,
  bottom: 30,
  left: 30
}

var width = svgWidth - margin.left - margin.right
var height = svgHeight - margin.top - margin.bottom

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select("#scatter")
  .append("svg")
  // .classed("chart", true)
  .attr("width", svgWidth)
  .attr("height", svgHeight)

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
      if (data[i].Degree_Attainment.startsWith("Total")){
        total.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Degree_Attainment.startsWith("Men")){
        men.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Degree_Attainment.startsWith("Women")){
        women.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Degree_Attainment.startsWith("White")){
        white.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Degree_Attainment.startsWith("Black")){
        black.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Degree_Attainment.startsWith("Asian")){
        asian.push(
          {degree: data[i].Degree_Attainment, Employed: data[i].Employed, Unemployed: data[i].Unemployed}
        )
      }
      else if (data[i].Degree_Attainment.startsWith("Hispanic")){
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
      .range(['#E41A1C','#377EB8'])
  
    
    chartGroup.select(".bars").remove()

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
    })
}

update("total")