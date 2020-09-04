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
/**
* Api interfact to a lab instance
*/

import { get, post, put, putFormData } from './util/apiHelper';

export const fetchDatasets = () => get('http://lab:5080/api/userdatasets');
export const fetchDataset = (id) => get(`http://lab:5080/api/datasets/${id}`);
export const putDataset = (params) => putFormData(`http://lab:5080/api/v1/datasets/`, params);//, true, 'multipart/form-data');


export const fetchDatasetMetafeatures = (id) => get(`http://lab:5080/api/v1/files/${id}/metafeatures`);

export const fetchMachines = () => get('http://lab:5080/api/v1/machines');

export const fetchExperiments = () => get('http://lab:5080/api/userexperiments');
export const fetchExperimentsParms = (parms) => post(`http://lab:5080/api/v1/experiments`, parms);
export const fetchExperiment = (id) => get(`http://lab:5080/api/v1/experiments/${id}`);

export const fetchAlgorithms = () => get('http://lab:5080/api/projects');

export const submitExperiment = (algorithm, params) => 
  post(`http://lab:5080/api/v1/projects/${algorithm}/experiment`, params);

export const updateAiStatus = (datasetId, aiStatus) =>
	put(`http://lab:5080/api/userdatasets/${datasetId}/ai`, {'ai':aiStatus});

export const getAiStatus = (datasetId) => get(`http://lab:5080/api/userdatasets/${datasetId}/ai`)

export const fetchExperimentModel = (id) => get(`http://lab:5080/api/v1/experiments/${id}/model`);
export const fetchExperimentScript = (id) => get(`http://lab:5080/api/v1/experiments/${id}/script`);

