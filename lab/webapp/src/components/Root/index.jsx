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
import React from 'react';
import { Provider } from 'react-redux';
import { Router, Route, IndexRedirect, hashHistory, IndexRoute } from 'react-router';


import App from '../App';
import Datasets from '../Datasets';
import FileUpload from '../FileUpload';
import Dataset from '../Dataset';
import Experiments from '../Experiments';
import Builder from '../Builder';
import Results from '../Results';
import Admin from '../Admin';
import NotFound from '../NotFound';
import ChatGPT from '../ChatGPT';
import ResultsV2 from '../ResultsV2';

import testTest from '../testTest';

/**
* Use react router to delineate different parts of website; essentially links
*/
function Root({ store }) {

  

  // var [eventsEnabled, setEventsEnabled] = React.useState(true)
  // var [open, setOpen] = React.useState(true)
  return (
    <Provider store={store}>
      <Router history={hashHistory} onUpdate={() => window.scrollTo(0, 0)}>
        <Route path="/" component={App}>
          <IndexRedirect to="datasets" />
          <Route path="upload_datasets" component={FileUpload} />
          <Route path="datasets" component={Datasets} />
          <Route path="datasets/:id" component={Dataset} />
          <Route path="experiments" component={Experiments} />
          {/* <Route path="builder" component={Builder} /> */}
          <Route path="builder" component={Builder} />
          {/* <Route path="/builder" render={(props) => <Builder {...props} />} /> */}
          {/* <Route path="results/:id" component={Results} /> */}
          <Route path="results/:id" component={ResultsV2} >

            {/* <IndexRoute component={ChatGPT}/>
            <Route path="test" component={testTest} /> */}

          </Route>
          {/* <Route path="results/:id" component={ChatGPT} /> */}
          <Route path="admin" component={Admin} />
          <Route path="*" component={NotFound} />
        </Route>
      </Router>
    </Provider>
    
  );
  
}

export default Root;





