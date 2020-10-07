/* ~This file is part of the PennAI library~

Copyright (C) 2017 Epistasis Lab, University of Pennsylvania

PennAI is maintained by:
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
import * as api from './api';
export const FETCH_PREFERENCES_REQUEST = 'FETCH_PREFERENCES_REQUEST';
export const FETCH_PREFERENCES_SUCCESS = 'FETCH_PREFERENCES_SUCCESS';
export const FETCH_PREFERENCES_FAILURE = 'FETCH_PREFERENCES_FAILURE';

export const fetchPreferences = () => (dispatch) => {
  dispatch({
    type: FETCH_PREFERENCES_REQUEST
  });

  return api.fetchPreferences().then(
    preferences => {
      dispatch({
        type: FETCH_PREFERENCES_SUCCESS,
        payload: preferences[0]
      });
    },
    error => {
      dispatch({
        type: FETCH_PREFERENCES_FAILURE,
        payload: error.message || 'Something went wrong.'
      });
    }
  );
};