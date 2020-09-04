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
import { getIsFetching } from './index';

export const PREFERENCES_FETCH_REQUEST = 'PREFERENCES_FETCH_REQUEST';
export const PREFERENCES_FETCH_SUCCESS = 'PREFERENCES_FETCH_SUCCESS';
export const PREFERENCES_FETCH_FAILURE = 'PREFERENCES_FETCH_FAILURE';

export const fetchPreferences = () => (dispatch, getState) => {
  if(getIsFetching(getState())) {
    return Promise.resolve();
  }

  dispatch({
    type: PREFERENCES_FETCH_REQUEST
  });

  return api.fetchPreferences().then(
    response => {
      dispatch({
        type: PREFERENCES_FETCH_SUCCESS,
        receivedAt: Date.now(),
        response
      });
    },
    error => {
      dispatch({
        type: PREFERENCES_FETCH_FAILURE,
        receivedAt: Date.now(),
        message: error.message || 'Something went wrong.'
      });
    }
  );
};