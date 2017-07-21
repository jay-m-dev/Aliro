import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as actions from './data/actions';
import { 
  getResults, 
  getIsFetching, 
  getErrorMessage
} from './data';
import SceneHeader from '../SceneHeader';
import Results from './Results';

class ResultsContainer extends Component {
  componentWillMount() {
    this.props.clearResults();
  }

  componentDidMount() {
    this.props.fetchResults(this.props.params.id);
  }

  getSceneHeader() {
    const { results } = this.props;
    if(results.size) {
      return {
        header: `Results: ${results.get('dataset_name')}`,
        subheader: `Experiment: #${results.get('_id')}`
      };
    }

    return { header: 'Results', subheader: null };
  }

  render() {
    const sceneHeader = this.getSceneHeader();
    return (
      <div>
        <SceneHeader header={sceneHeader.header} subheader={sceneHeader.subheader} />
        <Results {...this.props} />
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  results: getResults(state),
  isFetching: getIsFetching(state),
  errorMessage: getErrorMessage(state)
});

export default connect(
  mapStateToProps, 
  actions
)(ResultsContainer);