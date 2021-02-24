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
import React from 'react';
import { Segment, Header, Progress } from 'semantic-ui-react';
import { formatAlgorithm } from '../../../../../../utils/formatter';



function BestResult({ result, hasMetadata }) {
  const getNoResultMessage = () => {
    if(!hasMetadata) {
      return 'You must upload a metadata file in order to use this dataset.';
    }

    return 'No results yet, build a new experiment to start.';
  };

  const getResultLink = () => `/#/results/${result._id}`;

  const getPercent = () => (result.score * 100).toFixed(2);
  
  const getValue = () => (result.score).toFixed(2);

  const renderProgressBar = (result) => {
    switch(result.prediction_type) {
      case 'classification':
        return (
          <Progress
            inverted
            progress
            percent={getPercent()}
            className="accuracy-score"
            label="Balanced Accuracy"
          />
        );
      case 'regression':
        return (
          <Progress
            inverted
            progress='value'
            value={getValue()}
            total='1'
            className="accuracy-score"
            label="R^2"
          />
        );
      default:
        return;
    }
  }


  if(!result) {
    return (
      <Segment inverted attached className="panel-body">
        {getNoResultMessage()}
      </Segment>
    );
  }


  return (
    <Segment
      inverted
      attached
      href={getResultLink()}
      className="panel-body best-result"
    >
      <Header inverted size="small">
        {'Best Result'}
        <Header.Subheader>
          <div>{formatAlgorithm(result.algorithm)}</div>
          <span>{`#${result._id}`}</span>
        </Header.Subheader>
      </Header>
      { renderProgressBar(result) }
    </Segment>
  );
}

export default BestResult;