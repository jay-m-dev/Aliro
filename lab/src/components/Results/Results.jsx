import React, { Component } from 'react';
import FetchError from '../FetchError';
import SceneWrapper from '../SceneWrapper';
import { Gauge } from './components/Gauge';
import { Header, Grid, Segment, Icon, Image, Progress } from 'semantic-ui-react';
import moment from 'moment';
import twix from 'twix';

// if results does not exist, then go to not found page or error message!!
class Results extends Component {
	getFormattedDate(date) {
		return moment(date).format('M/DD/YY h:mm a');
	}

	getDuration(started, finished) {
		let duration = moment(started).twix(finished).asDuration();
		return `${duration._data.hours}h ${duration._data.minutes}m ${duration._data.seconds}s`;
	}

	getPercent(score) {
		return (score * 100).toFixed(2);
	}

	render() {
		
		const { 
			results,
			isFetching,
			errorMessage,
			fetchResults,
			confusionMatrix,
			rocCurve
		} = this.props;

		if(errorMessage) {
			return (
				<FetchError 
					message={errorMessage}
					onRetry={() => fetchResults(this.props.params.id)}
				/>
			);
		} else if(isFetching) {
			return (
				<Header 
					inverted 
					size="small"
					content="Retrieving your results..."
				/>
			);
		} else if(!isFetching && !results.size) {
			return (
				<Header 
					inverted 
					size="small"
					content="This result does not appear to exist."
				/>
			);
		}

		return (
			<SceneWrapper
				headerContent={`Results: ${results.get('dataset_name')}`}
				subheader={`Experiment: #${results.get('_id')}`}
			>
				<div className="results-scene">
					<Grid columns={3} stackable>
						<Grid.Row>
							<Grid.Column>
								<Segment inverted attached="top" className="panel-header">
									<Header inverted size="medium" content="Algorithm" />
								</Segment>
								<Segment inverted attached="bottom">	
									<Header inverted size="small" content={results.get('algorithm')} />
										<Grid columns={2}>
										{results.get('params').entrySeq().map(([param, value]) =>
											<Grid.Column key={param}>
												<Header
													inverted
													size="tiny"
													color="grey"
													content={param}
													subheader={value.toString()}
												/>
											</Grid.Column>
										)}
									</Grid>
								</Segment>
								<Segment inverted attached="top" className="panel-header">
									<Header inverted size="medium" content="Run Details" />
								</Segment>
								<Segment inverted attached="bottom">	
									<Grid columns={2}>
										<Grid.Column>
											<Header 
												inverted 
												color="grey" 
												size="tiny" 
												content="Started" 
												subheader={this.getFormattedDate(results.get('started'))}
											/>
										</Grid.Column>
										<Grid.Column>
											<Header 
												inverted 
												color="grey" 
												size="tiny" 
												content="Finished"
												subheader={this.getFormattedDate(results.get('finished'))}
											/>
										</Grid.Column>
										<Grid.Column>
											<Header 
												inverted 
												color="grey" 
												size="tiny" 
												content="Duration"
												subheader={this.getDuration(
													results.get('started'), 
													results.get('finished')
												)}
											/>
										</Grid.Column>
										<Grid.Column>
											<Header 
												inverted 
												color="grey" 
												size="tiny" 
												content="Launched By"
												subheader={results.get('launched_by')}
											/>
										</Grid.Column>
									</Grid>
								</Segment>
							</Grid.Column>
							<Grid.Column>
								<Segment inverted attached="top" className="panel-header">
									<Header 
										inverted
										size="medium"
										content="Confusion Matrix" 
									/>
								</Segment>
								<Segment inverted attached="bottom">	
									{confusionMatrix ? (
										<Image src={confusionMatrix} />
									) : (
										<span>Not available</span>
									)}
								</Segment>
								<Segment inverted attached="top" className="panel-header">
									<Header 
										inverted
										size="medium"
										content="ROC Curve" 
									/>
								</Segment>
								<Segment inverted attached="bottom">	
									{rocCurve ? (
										<Image src={rocCurve} />
									) : (
										<span>Not available</span>
									)}
								</Segment>
							</Grid.Column>
							<Grid.Column>
								<Segment inverted attached="top" className="panel-header">
									<Header 
										inverted
										size="medium"
										content="Training Accuracy" 
									/>
								</Segment>
								<Segment inverted attached="bottom">	
									<Gauge 
										chartName="training" 
										color="#7D5BA6"
										value={results.getIn(['scores', 'train_score'])}
									/>
								</Segment>
								<Segment inverted attached="top" className="panel-header">
									<Header 
										inverted
										size="medium"
										content="Testing Accuracy" 
									/>
								</Segment>
								<Segment inverted attached="bottom">	
									<Gauge 
										chartName="testing" 
										color="#55D6BE"
										value={results.getIn(['scores', 'test_score'])}
									/>
								</Segment>
								<Segment inverted attached="top" className="panel-header">
									<Header 
										inverted
										size="medium"
										content="AUC" 
									/>
								</Segment>
								<Segment inverted attached="bottom">	
									<Gauge 
										chartName="auc" 
										color="#59ABE3"
										value={results.getIn(['scores', 'roc_auc_score'])}
									/>
								</Segment>
							</Grid.Column>
						</Grid.Row>
					</Grid>
				</div>
			</SceneWrapper>
		);
	}
}

export default Results;

/*
<Grid.Column>
	<Segment inverted attached="top" className="panel-header">
		<Header 
			inverted
			size="medium"
			content="Training Accuracy" 
		/>
	</Segment>
	<Segment inverted attached="bottom">	
		<Gauge 
			chartName="training" 
			color="#7D5BA6"
			value={results.getIn(['scores', 'train_score'])}
		/>
	</Segment>
	<Segment inverted attached="top" className="panel-header">
		<Header 
			inverted
			size="medium"
			content="Testing Accuracy" 
		/>
	</Segment>
	<Segment inverted attached="bottom">	
		<Gauge 
			chartName="testing" 
			color="#55D6BE"
			value={results.getIn(['scores', 'test_score'])}
		/>
	</Segment>
	<Segment inverted attached="top" className="panel-header">
		<Header 
			inverted
			size="medium"
			content="AUC" 
		/>
	</Segment>
	<Segment inverted attached="bottom">	
		<Gauge 
			chartName="auc" 
			color="#59ABE3"
			value={results.getIn(['scores', 'roc_auc_score'])}
		/>
	</Segment>
</Grid.Column>
*/

/*
<Progress 
	inverted
	color="blue"
	progress
	percent={this.getPercent(results.getIn(['scores', 'train_score']))}
	className="train score"
/>
<Progress 
	inverted
	color="blue"
	progress
	percent={this.getPercent(results.getIn(['scores', 'test_score']))}
	className="test score"
/>
<Progress 
	inverted
	color="blue"
	progress
	percent={this.getPercent(results.getIn(['scores', 'roc_auc_score']))}
	className="auc score"
/>
*/