/* ~This file is part of the PennAI library~

Copyright (C) 2017 Epistasis Lab, University of Pennsylvania

PennAI is maintained by:
    - Heather Williams (hwilli@upenn.edu)
    - Weixuan Fu (weixuanf@pennmedicine.upenn.edu)
    - William La Cava (lacava@upenn.edu)
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

*/
process.env.MACHINE_CONFIG = './test/test_machine_config.json'
const machine_utils = require('../machine_utils.js');
const assert = require('assert');

var algorithms = ["DecisionTreeClassifier","GradientBoostingClassifier","KNeighborsClassifier"]
var project_list = machine_utils.getProjects(algorithms)
var projects = {};
project_list.forEach(function (value, i) {
    projects[algorithms[i]] = value;
});

describe('Mocha Test for getProjects function', function () {
  it('Test the total number of algorithms is the same with config.', function () {
        assert.equal(project_list.length, algorithms.length);
    });

  it('Test the name and order of algorithms is the same with config.', () => {
        for (var i in project_list) {
            var algo = project_list[i].name;
            var algo_conf = algorithms[i];
            assert.equal(algo_conf, algo);
        }
    });

});

describe('Mocha Test for getCapacity function', function () {
  it('Test getCapacity returns the correct capacity.', function () {
        assert.equal(machine_utils.getCapacity("DecisionTreeClassifier", 1, projects), 1);
    });

  it('Test getCapacity returns the correct capacity when maxCapacity=2.', function () {
        assert.equal(machine_utils.getCapacity("GradientBoostingClassifier", 2, projects), 2);
    });
});


describe('Mocha Test for checkCapacity function', function () {
  it('Test checkCapacity returns the correct values.', function () {
        ret = machine_utils.checkCapacity("DecisionTreeClassifier", 0, projects);
        assert.equal(ret.capacity, 0);
        assert.equal(ret.error_msg.error, "No machine capacity available");
    });

  it('Test checkCapacity returns the correct values when projId is not defined', function () {
        ret = machine_utils.checkCapacity("DecisionTreeClassifie", 2, projects);
        assert.equal(ret.capacity, 0);
        assert.equal(ret.error_msg.error, "Project 'DecisionTreeClassifie' does not exist");
    });

});
