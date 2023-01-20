/* ~This file is part of the Aliro library~

Copyright (C) 2023 Epistasis Lab, 
Center for Artificial Intelligence Research and Education (CAIRE),
Department of Computational Biomedicine (CBM),
Cedars-Sinai Medical Center.

Aliro is maintained by:
    - Hyunjun Choi (hyunjun.choi@cshs.org)
    - Miguel Hernandez (miguel.e.hernandez@cshs.org)
    - Nick Matsumoto (nicholas.matsumoto@cshs.org)
    - Jay Moran (jay.moran@cshs.org)
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
class LineChart extends Component {


  // train_sizes={train_sizes}
  // train_scores={train_scores}
  // test_scores={test_scores}
  // chartKey={chartKey}
  // chartColor={chartColor}
  // min={0.5}
  // max={1.0}

  componentDidMount() {
    const { train_sizes, train_scores, test_scores, chartKey, chartColor, min, max } = this.props;
    train_sizes && train_scores &&  test_scores && this.renderChart(train_sizes, train_scores, test_scores, chartKey, chartColor, min, max);
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

  // renderChart(expList, chartKey, chartColor, min, max) {
  renderChart(train_sizes, train_scores, test_scores, chartKey, chartColor, min, max) {

    window.console.log('here in renderChart for linechart');
    // window.console.log('train_sizes: ', train_sizes);
    // window.console.log('train_scores.length: ', train_scores.length);
    // window.console.log('train_scores: ', train_scores);
    // window.console.log('test_scores: ', test_scores);

    // // 
    // min = 0;
    // // max is last element in train_sizes
    max = train_sizes[train_sizes.length - 1];
    max = max + 0.1 * max;

    window.console.log('max: ', max);
    var total_train_scores=[];
    var total_test_scores=[];
    for (var i = 0; i < train_scores.length; i++) {
      
      // calculate averge of train_sizes[i]
      // divide by train_scores[i].length

      var sum_train_scores = 0;
      var sum_test_scores = 0;
      for (var j = 0; j < train_scores[i].length; j++) {
        sum_train_scores += train_scores[i][j];
        sum_test_scores += test_scores[i][j];
      }
      var avg_sum_train_scores = sum_train_scores / train_scores[i].length;
      var avg_sum_test_scores = sum_test_scores / test_scores[i].length;

      total_train_scores.push(avg_sum_train_scores);
      total_test_scores.push(avg_sum_test_scores);
      

    }

    
    var json = [];
    for (var i = 0; i < train_sizes.length; i++) {
      json.push({x: train_sizes[i], Training_score: total_train_scores[i], Cross_validation_score: total_test_scores[i]});
    }

    // window.console.log('json: ', json);

    // window.console.log('chartKey: ', chartKey);

    var chart = c3.generate({
      bindto: `.${chartKey}`,
      
      data: {
        json: json,

        keys: {
          x: 'x',
          value: ['Training_score', 'Cross_validation_score'],
      }
      
    },
      axis: {
        y: {
          min: 0,
          max: 1,
          label: 'Score'

        },
        x: {
          min: 0,
          max: max,
          label: 'Training examples',
          tick: {
            multiline:false,
            culling: false // <-- THIS!
          }

      }
    },
    grid: {
      y: {
        show: true,
        color : '#fff!important'
      },
      x: {
        show: true,
        color : '#fff!important'
      }
    },

    tooltip: {
      format: {
        title: function (d) { return 'Training examples: ' + d; }
      }
    }


    


  });

    // if document element has testuser text, then make it unvisiable 


    



  }

  render() {
    return (
      <div className={`LineChart ${this.props.chartKey}`} />
    );
  }
}

LineChart.defaultProps = {
  chartColor: '#60B044'
};

export default LineChart;











// test version
// class LineChart extends Component {
//   componentDidMount() {
//     const { expList, chartKey, chartColor, min, max } = this.props;
//     expList && this.renderChart(expList, chartKey, chartColor, min, max);
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

//   renderChart(expList, chartKey, chartColor, min, max) {
//     // window.console.log('exp list: ');
//     // window.console.log('exp list: ', expList);
//     // print d3 version
//     window.console.log('d3 version: ', d3.version);
//     // print c3 version
//     window.console.log('c3 version: ', c3.version);



//     // make expList like[['1',0.2],['2',0.3],['3',0.5]]
//     // expList = [['1',0.2],['2',0.3],['3',0.5]];

//     // print expList
//     window.console.log('expList: ', expList);

//     // print chartKey
//     window.console.log('chartKey: ', chartKey);

//     // var chart = c3.generate({
//     //   bindto: `.${chartKey}`,
//     //   data: {
          

//     //       columns:expList
//     //       ,
          
//     //       type : 'LineChart',
//     //       // colors: {
//     //       //   columns[0][0]: '#ff0000',
//     //       //   columns[1][0]: '#00ff00'
//     //       // }
//     //       // ,
//     //       onclick: function (d, i) { console.log("onclick", d, i); },
//     //       onmouseover: function (d, i) { console.log("onmouseover", d, i); },
//     //       onmouseout: function (d, i) { console.log("onmouseout", d, i); }
//     //   },
//     //   LineChart: {
//     //       // title: "Iris Petal Width"
//     //       title: ""
//     //       // title: expList
//     //   }
//     // });




//      // make confusion matrix [[10,20],[30,40]] using d3.js
//     var matrix = [[10,20],[30,40]];
   


//     // print curreht class name
//     window.console.log('current class name: ', `.${chartKey}`);

    

//       var div = d3.select(`.${chartKey}`)
//       // add svg to div 
//       var svg = div.append("svg")

//       var rect = svg.selectAll("rect")
//       .data(matrix)
//       .enter()
//       .append("rect")
//       .attr("width", 100)
//       .attr("height", 100)
//       // make width and height related to current div size
//       // .attr("width", function(d, i) {
//       //   return d3.select(`.${chartKey}`).node().getBoundingClientRect().width/10;
//       // })
//       // .attr("height", function(d, i) {
//       //   return d3.select(`.${chartKey}`).node().getBoundingClientRect().height/10;
//       // })
//       .attr("x", function(d, i) {
//         return i * 50;
//       } )
//       .attr("y", function(d, i) {
//         return i * 50;
//       }
//       )
//       .attr('id', function(d, i) {
//         return 'rect_' + i;
//       }
//       )
//       .attr('fill', function(d, i) {
//         return 'red';
//       } 
//       )
//       // make it show more than background color
//       .attr('opacity', 0.5)
//       // add mouseover event
//       .on("mouseover", function(d, i) {
//         // change color
//         d3.select(this).attr('fill', 'blue');
//         console.log('number',d)
//         // show this d as string on the rect
//         d3.select(this).text(d);
//         // make the text color white
//         d3.select(this).attr('fill', 'white');

//         d3.select(this).text('This is some information about whatever')
//                 .attr('x', 50)
//                 .attr('y', 150)
//                 .attr('fill', 'white')

//       })
//       .append('text').text('test');
//       // add data value to each rect text


//       // matrix 
//       //  20  30
//       //  40  50

//       // add the matrix value to rect 

//       // var text = svg.selectAll("text")
//       // .data(matrix)
//       // .enter()
//       // .append("text")


  

//   }

//   render() {
//     return (
//       <div className={`LineChart ${this.props.chartKey}`} />
//     );
//   }
// }

// LineChart.defaultProps = {
//   chartColor: '#60B044'
// };

// export default LineChart;







