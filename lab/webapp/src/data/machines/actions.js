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
import * as api from './api';
export const FETCH_MACHINES_REQUEST = 'FETCH_MACHINES_REQUEST';
export const FETCH_MACHINES_SUCCESS = 'FETCH_MACHINES_SUCCESS';
export const FETCH_MACHINES_FAILURE = 'FETCH_MACHINES_FAILURE';
export const FETCH_ENV_VARS_REQUEST = 'FETCH_ENV_VARS_REQUEST';
export const FETCH_ENV_VARS_SUCCESS = 'FETCH_ENV_VARS_SUCCESS';
export const FETCH_ENV_VARS_FAILURE = 'FETCH_ENV_VARS_FAILURE';

export const fetchMachines = () => (dispatch) => {
  dispatch({
    type: FETCH_MACHINES_REQUEST
  });

  return api.fetchMachines().then(
    machines => {
      dispatch({
        type: FETCH_MACHINES_SUCCESS,
        payload: machines
      });
    },
    error => {
      dispatch({
        type: FETCH_MACHINES_FAILURE,
        payload: error.message || 'Something went wrong.'
      });
    }
  );
};

export const fetchEnvVars = () => (dispatch) => {
  dispatch({
    type: FETCH_ENV_VARS_REQUEST
  });

  return api.fetchEnvVars().then(
    envVar => {
      dispatch({
        type: FETCH_ENV_VARS_SUCCESS,
        payload: envVar
      });
    },
    error => {
      dispatch({
        type: FETCH_ENV_VARS_FAILURE,
        payload: error.message || 'Something went wrong.'
      });
    }
  );
};
