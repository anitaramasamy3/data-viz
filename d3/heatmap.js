var data=[]
var s1=[];
var s2=[];
var s3=[];
var s4=[];
var s5=[];
var s6=[];
d3.csv('heatmap.csv', function(d){

  dataa=[
    [house= 1,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Baratheon)],
    [house= 2,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Greyjoy)],
    [house= 3,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Lannister)],
    [house= 4,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Martell)],
    [house= 5,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Stark)],
    [house= 6,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Targaryen)],
    [house= 7,
    episode= parseInt(d.episode),
    season= parseInt(d.season),
    value= parseInt(d.Tyrell)]];
    return dataa;

}, function(error, rows){
  data=rows;
  splitData(rows);

});

function splitData(fulldata){


  var s = ["1", "2", "3","4","5","6"];
  var select = d3.select('#season')
    .append('select')
    	.attr('class','select')
      .on('change',onchange)

      var options = select
        .selectAll('option')
      	.data(s).enter()
      	.append('option')
      		.text(function (d) { return d; });


  for(var i=0;i<fulldata.length;i++){
    for(var j=0;j<7;j++){

    if(fulldata[i][j][2]==1){
      temp={house:fulldata[i][j][0],
            episode:fulldata[i][j][1],
            value:fulldata[i][j][3]};
      s1.push(temp);

    }
    if(fulldata[i][j][2]==2){
      temp={house:fulldata[i][j][0],
            episode:fulldata[i][j][1],
            value:fulldata[i][j][3]};
      s2.push(temp);
    }
    if(fulldata[i][j][2]==3){
      temp={house:fulldata[i][j][0],
            episode:fulldata[i][j][1],
            value:fulldata[i][j][3]};
      s3.push(temp);
    };
    if(fulldata[i][j][2]==4){
      temp={house:fulldata[i][j][0],
            episode:fulldata[i][j][1],
            value:fulldata[i][j][3]};
      s4.push(temp);
    }
    if(fulldata[i][j][2]==5){
      temp={house:fulldata[i][j][0],
            episode:fulldata[i][j][1],
            value:fulldata[i][j][3]};
      s5.push(temp);
    }
    if(fulldata[i][j][2]==6){
      temp={house:fulldata[i][j][0],
            episode:fulldata[i][j][1],
            value:fulldata[i][j][3]};
      s6.push(temp);
    }
  }
  }
  console.log('season1'+s1)
  plotheat(s1);

};
function onchange() {
  d3.select("svg").remove();
  selectValue = d3.select('select').property('value')
  console.log("cats"+selectValue);
  if(selectValue==1){
    plotheat(s1);
  }
  if(selectValue==2){
    console.log('s2'+s2[0])
    plotheat(s2);
  }
  if(selectValue==3){
    plotheat(s3);
  }
  if(selectValue==4){
    plotheat(s4);
  }
  if(selectValue==5){
    plotheat(s5);
  }
  if(selectValue==6){
    plotheat(s6);
  }
};
function plotheat(data){

  var margin = { top: 50, right: 0, bottom: 100, left: 100 },
            width = 960 - margin.left - margin.right,
            height = 530 - margin.top - margin.bottom,
            gridSize = Math.floor(width / 20),
            legendElementWidth = gridSize *1.5,
            buckets = 9,
            colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], 

            house = ["Baratheon", "Greyjoy", "Lannister", "Martell", "Stark", "Targaryen", "Tyrell"],
            episode = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
  //svg
  var svg = d3.select("#chart").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  //add houses
  var houseLabels = svg.selectAll(".houseLabel")
          .data(house)
          .enter().append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return i * gridSize; })
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
            .attr("class", function (d, i) { return ((i >= 0 && i <= 6) ? "houseLabel mono axis axis-workweek" : "houseLabel mono axis"); });
  //add episodes
  var episodeLabels = svg.selectAll(".episodeLabel")
          .data(episode)
          .enter().append("text")
            .text(function(d) { return d; })
            .attr("x", function(d, i) { return i * gridSize; })
            .attr("y", gridSize*7 + 30)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)")
            .attr("class", function(d, i) { return "episodeLabel mono axis axis-worktime" });
  //heatmap
  var colorScale = d3.scale.quantile()
              .domain([0, buckets - 1, d3.max(data, function (d) { return d.value; })])
              .range(colors);
              svg.append("text")
                .text('Episode')
                .attr('class','houseLabel monob axis axis-workweek')
                .attr('x',gridSize*10 + 20)
                .attr('y',gridSize*8 - 20);
  svg.append("text")
    .text('Number of Appearances')
    .attr('class','houseLabel monob axis axis-workweek')
    .attr('x',0)
    .attr('y',gridSize*7 +60);
    svg.append("text")
      .text('House')
      .attr('class','houseLabel monob axis axis-workweek')
      .attr('x',-gridSize)
      .attr('y',-10);
  var cards = svg.selectAll(".episode")
              .data(data, function(d) {return d.house+':'+d.episode;});

  cards.append("title");
  cards.enter().append("rect")
              .attr("x", function(d) { return (d.episode - 1) * gridSize; })
              .attr("y", function(d) { return (d.house - 1) * gridSize; })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("class", "episode bordered")
              .attr("width", gridSize)
              .attr("height", gridSize)
              .style("fill", colors[0]);

  cards.transition().duration(1000)
              .style("fill", function(d) { return colorScale(d.value); });

  cards.select("title").text(function(d) { return d.value; });

  cards.exit().remove();
  var legend = svg.selectAll(".legend")
              .data([0].concat(colorScale.quantiles()), function(d) { return d; });

          legend.enter().append("g")
              .attr("class", "legend");

          legend.append("rect")
            .attr("x", function(d, i) { return legendElementWidth * i; })
            .attr("y", height)
            .attr("width", legendElementWidth)
            .attr("height", gridSize / 2)
            .style("fill", function(d, i) { return colors[i]; });

          legend.append("text")
            .attr("class", "mono")
            .text(function(d) { return Math.round(d); })
            .attr("x", function(d, i) { return legendElementWidth * i; })
            .attr("y", height + gridSize);

          legend.exit().remove();

};
