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
var Promise = require("bluebird");
var db = require("./db").db;
exports.validateParams = function(projId, options, datasetId, callback) {
    var prevExp = db.experiments.find({
        _dataset_id: db.toObjectID(datasetId),
        _project_id: db.toObjectID(projId),
        _options: options,
        _status: "success"
    }).toArrayAsync();
    Promise.all(prevExp)
        .then((results) => {
            if (results.length >= 1) {
                error = {
                    error: "already exists"
                };
                callback(error);
            } else {
                success = {
                    success: "Options validated"
                };
                callback(success);
            }
        })
        .catch((err) => {
            error = {
                error: err
            };
            callback(error);

        });

}
