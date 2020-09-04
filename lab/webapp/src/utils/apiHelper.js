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
require('es6-promise').polyfill();
import fetch from 'isomorphic-fetch';

export const get = (route) => {
  return fetch(route, {
    credentials: 'include'
  })
    .then(response => {
      if(response.status >= 400) {
        throw new Error(`${response.status}: ${response.statusText}`);
      }
      return response.json();
    })
    .then(json => json);
};

export const getFile = (route) => {
  return fetch(route, {
    credentials: 'include'
  })
    .then(response => {
      if(response.status >= 400) {
        throw new Error(`${response.status}: ${response.statusText}`);
      }
      return response.blob();
    })
    .then(json => json);
};

export const post = (route, body) => {
  let myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');

  return fetch(route, {
    method: 'POST',
    credentials: 'include',
    headers: myHeaders,
    mode: 'cors',
    cache: 'default',
    body: JSON.stringify(body)
  })
    .then(response => {
      if(response.status >= 400) {
        throw new Error(`${response.status}: ${response.statusText}`);
      }
      return response.json();
    })
    .then(json => json);
};

export const put = (route, body) => {
  let myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');

  return fetch(route, {
    method: 'PUT',
    credentials: 'include',
    headers: myHeaders,
    mode: 'cors',
    cache: 'default',
    body: JSON.stringify(body)
  })
    .then(response => {
      if(response.status >= 400) {
        throw new Error(`${response.status}: ${response.statusText}`);
      }
      return response.json();
    })
    .then(json => json);
};

export const uploadFile = (route, body) => {
  // using headers with content type - multipart/form-data results in an error
  // when trying to upload a file from a form
  // error in question - Error: Multipart: Boundary not found
  // don't need to pass headers when uploading files with - check here:
  // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  return fetch("/api/v1/datasets", {
    method: 'PUT',
    credentials: 'include',
    body: body
  }).then(response => {
      return response.json();
    })
    .catch((err) => {
           throw(err);
    })
    .then((json) => {
      //window.console.log('api helper json', json);
      return json;
    });
}
