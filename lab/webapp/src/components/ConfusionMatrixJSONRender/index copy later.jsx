/* ~This file is part of the Aliro library~

Copyright (C) 2017 Epistasis Lab, University of Pennsylvania

Aliro is maintained by:
    - Heather Williams (hwilli@upenn.edu)
    - Weixuan Fu (weixuanf@upenn.edu)
    - William La Cava (lacava@upenn.edu)
    - Michael Stauffer (stauffer@upenn.edu)
    - and many other generous open source contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

(Autogenerated header, do not modify)

*/
import React, { Component } from 'react';

import c3 from 'c3';

import d3 from 'd3';



// working version
// class TestLineChart extends Component {


//   // train_sizes={train_sizes}
//   // train_scores={train_scores}
//   // test_scores={test_scores}
//   // chartKey={chartKey}
//   // chartColor={chartColor}
//   // min={0.5}
//   // max={1.0}

//   componentDidMount() {
//     const { train_sizes, train_scores, test_scores, chartKey, chartColor, min, max } = this.props;
//     train_sizes && train_scores &&  test_scores && this.renderChart(train_sizes, train_scores, test_scores, chartKey, chartColor, min, max);
//   }
// /*
// colors: {
//   'test_score': '#0072b2',  ---- light blue
//   'train_score': '#f0e442'  ---- light yellow
//   '#55D6BE' ----- light sea green
// }

// use anonymous function to 'disable' interaction
// look here - https://github.com/c3js/c3/issues/493#issuecomment-456686654
// */

//   // renderChart(expList, chartKey, chartColor, min, max) {
//   renderChart(train_sizes, train_scores, test_scores, chartKey, chartColor, min, max) {

//     window.console.log('here in renderChart for TestLineChart');
//     // window.console.log('train_sizes: ', train_sizes);
//     // window.console.log('train_scores.length: ', train_scores.length);
//     // window.console.log('train_scores: ', train_scores);
//     // window.console.log('test_scores: ', test_scores);

//     // // 
//     // min = 0;
//     // // max is last element in train_sizes
//     max = train_sizes[train_sizes.length - 1];
//     max = max + 0.1 * max;

//     window.console.log('max: ', max);
//     var total_train_scores=[];
//     var total_test_scores=[];
//     for (var i = 0; i < train_scores.length; i++) {
      
//       // calculate averge of train_sizes[i]
//       // divide by train_scores[i].length

//       var sum_train_scores = 0;
//       var sum_test_scores = 0;
//       for (var j = 0; j < train_scores[i].length; j++) {
//         sum_train_scores += train_scores[i][j];
//         sum_test_scores += test_scores[i][j];
//       }
//       var avg_sum_train_scores = sum_train_scores / train_scores[i].length;
//       var avg_sum_test_scores = sum_test_scores / test_scores[i].length;

//       total_train_scores.push(avg_sum_train_scores);
//       total_test_scores.push(avg_sum_test_scores);
      

//     }

    
//     var json = [];
//     for (var i = 0; i < train_sizes.length; i++) {
//       json.push({x: train_sizes[i], Training_score: total_train_scores[i], Cross_validation_score: total_test_scores[i]});
//     }

//     // window.console.log('json: ', json);

//     // window.console.log('chartKey: ', chartKey);

//     var chart = c3.generate({
//       bindto: `.${chartKey}`,
      
//       data: {
//         json: json,

//         keys: {
//           x: 'x',
//           value: ['Training_score', 'Cross_validation_score'],
//       }
      
//     },
//       axis: {
//         y: {
//           min: 0,
//           max: 1,
//           label: 'Score'

//         },
//         x: {
//           min: 0,
//           max: max,
//           label: 'Training examples',
//           tick: {
//             multiline:false,
//             culling: false // <-- THIS!
//           }

//       }
//     },
//     grid: {
//       y: {
//         show: true,
//         color : '#fff!important'
//       },
//       x: {
//         show: true,
//         color : '#fff!important'
//       }
//     },

//     tooltip: {
//       format: {
//         title: function (d) { return 'Training examples: ' + d; }
//       }
//     }


    


//   });

//     // if document element has testuser text, then make it unvisiable 


    



//   }

//   render() {
//     return (
//       <div className={`TestLineChart ${this.props.chartKey}`} />
//     );
//   }
// }

// TestLineChart.defaultProps = {
//   chartColor: '#60B044'
// };

// export default TestLineChart;











// test version
class TestLineChart extends Component {
  componentDidMount() {
    
    // train_sizes={train_sizes}
    // train_scores={train_scores}
    // test_scores={test_scores}
    // chartKey={chartKey}
    // chartColor={chartColor}
    // min={0.5}
    // max={1.0}
    const { train_sizes,train_scores,test_scores, cnf_data,chartKey, chartColor, min, max } = this.props;
    this.renderChart(train_sizes,train_scores,test_scores,cnf_data, chartKey, chartColor, min, max);
  }

 
/*
colors: {
  'test_score': '#0072b2',  ---- light blue
  'train_score': '#f0e442'  ---- light yellow
  '#55D6BE' ----- light sea green
}

use anonymous function to 'disable' interaction
look here - https://github.com/c3js/c3/issues/493#issuecomment-456686654
*/

  renderChart(train_sizes,train_scores,test_scores,cnf_data, chartKey, chartColor, min, max) {
    console.log('here in renderChart for TestLineChart');
    

    var margin = {top: 50, right: 50, bottom: 100, left: 100};

    function Matrix(options) {
      var width = 250,
          height = 250,
          data = options.data,
          container = options.container,
          labelsData = options.labels,
          startColor = options.start_color,
          endColor = options.end_color;

      var widthLegend = 100;

      if(!data){
        throw new Error('Please pass data');
      }

      if(!Array.isArray(data) || !data.length || !Array.isArray(data[0])){
        throw new Error('It should be a 2-D array');
      }

            var maxValue = d3.max(data, function(layer) { return d3.max(layer, function(d) { return d; }); });
            var minValue = d3.min(data, function(layer) { return d3.min(layer, function(d) { return d; }); });

      var numrows = data.length;
      var numcols = data[0].length;
      var svg = d3.select(`.${chartKey}`).append("svg")
      // var svg = d3.select(container).append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var background = svg.append("rect")
          .style("stroke", "black")
          .style("stroke-width", "2px")
          .attr("width", width)
          .attr("height", height);

      var x = d3.scaleBand()
          .domain(d3.range(numcols))
          .range([0, width]);

      var y = d3.scaleBand()
          .domain(d3.range(numrows))
          .range([0, height]);

      var colorMap = d3.scaleLinear()
          .domain([minValue,maxValue])
          .range([startColor, endColor]);

      var row = svg.selectAll(".row")
          .data(data)
          .enter().append("g")
          .attr("class", "row")
          .attr("transform", function(d, i) { return "translate(0," + y(i) + ")"; });

      var cell = row.selectAll(".cell")
          .data(function(d) { return d; })
          .enter().append("g")
          .attr("class", "cell")
          .attr("transform", function(d, i) { return "translate(" + x(i) + ", 0)"; });

      cell.append('rect')
          .attr("width", x.bandwidth())
          .attr("height", y.bandwidth())
          .style("stroke-width", 0);

        cell.append("text")
          .attr("dy", ".32em")
          .attr("x", x.bandwidth() / 2)
          .attr("y", y.bandwidth() / 2)
          .attr("text-anchor", "middle")
          .style("fill", function(d, i) { return d >= maxValue/2 ? 'white' : 'black'; })
          .text(function(d, i) { return d; });

      row.selectAll(".cell")
          .data(function(d, i) { return data[i]; })
          .style("fill", colorMap);

      var labels = svg.append('g')
        .attr('class', "labels");

      var columnLabels = labels.selectAll(".column-label")
          .data(labelsData)
          .enter().append("g")
          .attr("class", "column-label")
          .attr("transform", function(d, i) { return "translate(" + x(i) + "," + height + ")"; });

      columnLabels.append("line")
        .style("stroke", "black")
          .style("stroke-width", "1px")
          .attr("x1", x.bandwidth() / 2)
          .attr("x2", x.bandwidth() / 2)
          .attr("y1", 0)
          .attr("y2", 5);

      columnLabels.append("text")
          .attr("x", 30)
          .attr("y", y.bandwidth() / 2)
          .attr("dy", ".22em")
          .attr("text-anchor", "end")
          .attr("transform", "rotate(-60)")
          .text(function(d, i) { return d; });

      var rowLabels = labels.selectAll(".row-label")
          .data(labelsData)
        .enter().append("g")
          .attr("class", "row-label")
          .attr("transform", function(d, i) { return "translate(" + 0 + "," + y(i) + ")"; });

      rowLabels.append("line")
        .style("stroke", "black")
          .style("stroke-width", "1px")
          .attr("x1", 0)
          .attr("x2", -5)
          .attr("y1", y.bandwidth() / 2)
          .attr("y2", y.bandwidth() / 2);

      rowLabels.append("text")
          .attr("x", -8)
          .attr("y", y.bandwidth() / 2)
          .attr("dy", ".32em")
          .attr("text-anchor", "end")
          .text(function(d, i) { return d; });

        var key = d3.select("#legend")
        .append("svg")
        .attr("width", widthLegend)
        .attr("height", height + margin.top + margin.bottom);

        var legend = key
        .append("defs")
        .append("svg:linearGradient")
        .attr("id", "gradient")
        .attr("x1", "100%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "100%")
        .attr("spreadMethod", "pad");

        legend
        .append("stop")
        .attr("offset", "0%")
        .attr("stop-color", endColor)
        .attr("stop-opacity", 1);

        legend
        .append("stop")
        .attr("offset", "100%")
        .attr("stop-color", startColor)
        .attr("stop-opacity", 1);

        key.append("rect")
        .attr("width", widthLegend/2-10)
        .attr("height", height)
        .style("fill", "url(#gradient)")
        .attr("transform", "translate(0," + margin.top + ")");

        var y = d3.scaleLinear()
        .range([height, 0])
        .domain([minValue, maxValue]);

        var yAxis = d3.axisRight(y);

        key.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(41," + margin.top + ")")
        .call(yAxis)

    }
    function testMatrix(){
      console.log("testMatrix");
    }
    var matrix = cnf_data;  

    console.log("cnf_data in line",cnf_data);
   


    // print curreht class name
    window.console.log('TestLine current class name: ', `.${chartKey}`);

    

    var div = d3.select(`.${chartKey}`)
    // add svg to div 
    
    var svg = div.append("svg")
    // make viewbox to make svg responsive
    .attr("viewBox", "0 0 600 400")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .append("g")
    .attr("transform", "translate(50,50)");

    
    // var matrix = [[10,20],[30,40]];


    // var matrix = [[10,20],[30,40]];



    var tempcount=0;
    
    

    // var rect = svg.selectAll("rect")
    // .data(matrix)
    // .enter()
    // .append("rect")
    // .attr("width", 100)
    // .attr("height", 100)
    // // make width and height related to current div size
    // // .attr("width", function(d, i) {
    // //   return d3.select(`.${chartKey}`).node().getBoundingClientRect().width/10;
    // // })
    // // .attr("height", function(d, i) {
    // //   return d3.select(`.${chartKey}`).node().getBoundingClientRect().height/10;
    // // })
    // .attr("x", function(d, i) {
    //   console.log('d: ', d);
      
    //   console.log('d[0][0]: ', d[0]);
    //   console.log('d[0][1]: ', d[1]);
    //   // loop based on size of d
    //   for (var i = 0; i < d.length; i++) {
    //     // console.log('d[i]: ', d[i]);
    //   // make 1 row 2 column
    //     tempcount+=1;
    //     console.log('tempcount', tempcount);
    //   }
      
    //   return i * 100;

    // } )
    // .attr("y", function(d, i) {

    //   return i * 100;
    // }
    // )
    // .attr('id', function(d, i) {
    //   return 'rect_' + d;
    // }
    // )
    // .attr('fill', function(d, i) {
      
    //   console.log('fill_d: ', d);
    //   // choose color based on value d
      
    //   if (d > 150) {
    //     return 'green';
    //   }
    //   return 'red';
    // } 
    // )
    // // make it show more than background color
    // .attr('opacity', 0.5)
    // // add mouseover event
    // // .on("mouseover", function(d, i) {
    // //   // change color
    // //   d3.select(this).attr('fill', 'blue');
    // //   console.log('number',d)
    // //   // show this d as string on the rect
    // //   d3.select(this).text(d);
    // //   // make the text color white
    // //   d3.select(this).attr('fill', 'white');

    // //   d3.select(this).text('This is some information about whatever')
    // //           .attr('x', 50)
    // //           .attr('y', 150)
    // //           .attr('fill', 'white')

    // // })
    // .append('text').text('test');


    // need to generalize this to work for any size matrix
  
    var tp = matrix[0][0];
    var fn = matrix[0][1];
    var fp = matrix[1][0];
    var tn = matrix[1][1];

    var p = tp + fn;
    var n = fp + tn;

    var accuracy = (tp+tn)/(p+n);
    var f1 = 2*tp/(2*tp+fp+fn);
    var precision = tp/(tp+fp);
    var recall = tp/(tp+fn);

    accuracy = Math.round(accuracy * 100) / 100
    f1 = Math.round(f1 * 100) / 100
    precision = Math.round(precision * 100) / 100
    recall = Math.round(recall * 100) / 100

    var computedData = [];
    computedData.push({"F1":f1, "PRECISION":precision,"RECALL":recall,"ACCURACY":accuracy});
      
    var labels = ['Class A', 'Class B'];
		Matrix({
			container : '#container',
      chartKey : chartKey,
			data      : matrix,
			labels    : labels,
            start_color : '#ffffff',
            end_color : '#e67e22'
		});
    // testMatrix();

		// rendering the table
    // var table = tabulate(computedData, ["F1", "PRECISION","RECALL","ACCURACY"]);

  

  }

  render() {
    return (
      <div className={`TestLineChart ${this.props.chartKey}`} />
    );
  }
}

TestLineChart.defaultProps = {
  chartColor: '#60B044'
};

export default TestLineChart;







