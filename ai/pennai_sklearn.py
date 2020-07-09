import numpy as np
import pandas as pd
import time
from datetime import datetime
import pickle
import json
import os
import warnings
import random
from ai.knowledgebase_utils import load_knowledgebase
from ai.metalearning.get_metafeatures import generate_metafeatures
from ai.metalearning.dataset_describe import Dataset
import logging
import sys
from ai.recommender.average_recommender import AverageRecommender
from ai.recommender.random_recommender import RandomRecommender
from ai.recommender.knn_meta_recommender import KNNMetaRecommender
from ai.metrics import SCORERS
from ai.recommender.surprise_recommenders import (
    CoClusteringRecommender,
    KNNWithMeansRecommender,
    KNNDatasetRecommender,
    KNNMLRecommender,
    SlopeOneRecommender,
    SVDRecommender)

from sklearn.model_selection import cross_val_score, ParameterGrid
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.exceptions import ConvergenceWarning
from joblib import Parallel, delayed
# ignore ConvergenceWarning in SVR and SVC
warnings.filterwarnings("ignore", category=ConvergenceWarning)

logger = logging.getLogger(__name__)


class PennAI(BaseEstimator):
    """Penn AI standalone sklearn wrapper.

    Responsible for:
    - checking for user requests for recommendations,
    - checking for new results from experiments,
    - calling the recommender system to generate experiment recommendations,
    - posting the recommendations to the API.
    - handling communication with the API.

    :param rec_class: ai.BaseRecommender - recommender to use
    :param verbose: int, 0 quite, 1 info, 2 debug
    :param warm_start: if it is a path of plk file, attempt to
            load the ai state from the plk file;
    :param scoring: str - scoring for evaluating recommendations
    :param n_recs: int - number of recommendations to make for each iteration
    :param n_iters: int = total number of iteration
    :param knowledgebase: file - input file for knowledgebase
    :param kb_metafeatures: inputfile for metafeature
    :param ml_p_file: inputfile for hyperparams space for all ML algorithms
    :param ensemble: if it is a integer N, PennAI will use
            VotingClassifier/VotingRegressor to ensemble
            top N best models into one model.
    :param max_time_mins: maximum time in minutes that PennAI can run # todo
    :param random_state: random state for recommenders
    :param n_jobs: int (default: 1) The number of cores to dedicate to
            computing the scores with joblib. Assigning this parameter to -1
            will dedicate as many cores as are available on your system.

    """
    mode = "classification"

    def __init__(self,
                 rec_class=None,
                 verbose=0,
                 warm_start=None,
                 scoring=None,
                 n_recs=10,
                 n_iters=10,
                 knowledgebase=None,
                 kb_metafeatures=None,
                 ml_p_file=None,
                 ensemble=None,
                 max_time_mins=None,
                 random_state=None,
                 n_jobs=1):
        """Initializes AI managing agent."""

        self.rec_class = rec_class
        self.verbose = verbose
        self.warm_start = warm_start
        self.scoring = scoring
        self.n_recs = n_recs
        self.n_iters = n_iters
        self.knowledgebase = knowledgebase
        self.kb_metafeatures = kb_metafeatures
        self.ml_p_file = ml_p_file
        self.ensemble = ensemble
        self.max_time_mins = max_time_mins
        self.random_state = random_state
        self.n_jobs = n_jobs

    def fit_init_(self):
        """
        fit initilization
        """

        # recommendation engines for different problem types
        # will be expanded as more types of probles are supported
        # (classification, regression, unsupervised, etc.)
        if self.scoring is not None:
            self.scoring_ = self.scoring

        # match scoring_ to metric in knowledgebase
        metric_match = {
            "accuracy": "accuracy",
            "balanced_accuracy": "bal_accuracy",
            "f1": "macrof1",
            "f1_macro": "macrof1",
            "r2": "r2_cv_mean",
            "explained_variance": "explained_variance_cv_mean",
            "neg_mean_squared_error": "neg_mean_squared_error_cv_mean"
        }
        self.metric_ = metric_match[self.scoring_]

        self.rec_engines = {
            self.mode: None
        }

        if self.verbose == 2:
            logger_level = logging.DEBUG
        elif self.verbose == 1:
            logger_level = logging.INFO
        elif self.verbose <= 0:
            logger_level = logging.ERROR

        logger.setLevel(logger_level)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(module)s: %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Request manager settings
        self.n_recs_ = self.n_recs if self.n_recs > 0 else 1

        self.initilize_recommenders(self.rec_class)  # set self.rec_engines

        # local dataframe of datasets and their metafeatures
        self.dataset_mf_cache = pd.DataFrame()

        if self.knowledgebase and self.kb_metafeatures:
            resultsData = self.load_kb()
        else:
            raise ValueError(
                "please provide knowledgebase and kb_metafeatures")

        # if there is a pickle file, load it as the recommender scores
        if self.warm_start:
            logger.info("Loading pickled recommender")
            self.rec_engines[self.mode].load(self.warm_start, resultsData)

    def generate_metafeatures_from_X_y(self, X, y):
        """
        Return meta_features based on input X and y in fit().
        :param X: pd.DataFrame
        :param y: pd.Series

        """
        df = X.copy()
        df['pennai_target'] = y
        dataset = Dataset(df=df,
                          dependent_col="pennai_target",
                          prediction_type=self.mode
                          )
        self.datasetId = dataset.m_data_hash()

        meta_features = generate_metafeatures(dataset)
        mf = [meta_features]
        df = pd.DataFrame.from_records(mf, columns=meta_features.keys())
        # include dataset name
        df['dataset'] = self.datasetId
        df.sort_index(axis=1, inplace=True)
        return df

    def valid_combo(self, combo, bad_combos):
        """Checks if parameter combination is valid."""
        for bad_combo in bad_combos:
            bc = {}
            for b in bad_combo:
                bc.update(b)
            bad = True
            for k, v in bc.items():
                if combo[k] != v:
                    bad = False
        return not bad

    def get_all_ml_p(self, categoryFilter=None):
        """
        Returns a list of ml and parameter options based on projects.json

        :returns: pd.DataFrame - unique ml algorithm and parameter combinations
            with columns 'alg_name', 'category', 'alg_name', 'parameters'
            'parameters' is a dictionary of parameters
        """

        if self.ml_p_file is None:
            self.ml_p_file_ = "docker/dbmongo/files/projects.json"
        else:
            self.ml_p_file_ = self.ml_p_file

        self.algorithms = json.load(open(self.ml_p_file_, encoding="utf8"))
        # exclude algorithm in different mode
        self.algorithms = [
            a for a in self.algorithms if a['category'] == self.mode]

        result = []  # returned value
        good_def = True  # checks that json for ML is in good form

        for i, x in enumerate(self.algorithms):
            logger.debug('Checking ML: ' + str(x['name']))

            hyperparams = x['schema'].keys()
            hyperparam_dict = {}
            if 'static_parameters' in x:
                self.static_parameters[x['name']] = x['static_parameters']
            else:
                self.static_parameters[x['name']] = {}
            # get a dictionary of hyperparameters and their values
            for h in hyperparams:
                logger.debug('  Checking hyperparams: x[''schema''][h]' +
                             str(x['schema'][h]))
                if 'ui' in x['schema'][h]:
                    if 'values' in x['schema'][h]['ui']:
                        hyperparam_dict[h] = x['schema'][h]['ui']['values']
                    else:
                        hyperparam_dict[h] = x['schema'][h]['ui']['choices']
                else:
                    good_def = False
            if good_def:
                all_hyperparam_combos = list(ParameterGrid(hyperparam_dict))
                #print('\thyperparams: ',hyperparam_dict)
                logger.debug(
                    '{} hyperparameter combinations for {}'.format(
                        len(all_hyperparam_combos), x['name']))
                # print(all_hyperparam_combos)

                for ahc in all_hyperparam_combos:
                    if 'invalidParameterCombinations' in x.keys():
                        if not self.valid_combo(
                                ahc, x['invalidParameterCombinations']):
                            continue
                    result.append({'algorithm': x['name'],
                                   'category': x['category'],
                                   'parameters': ahc,
                                   'alg_name': x['name']})
            else:
                logger.error('warning: ' + str(x['name']) + 'was skipped')
            good_def = True

        # convert to dataframe, making sure there are no duplicates
        all_ml_p = pd.DataFrame(result)
        tmp = all_ml_p.copy()
        tmp['parameters'] = tmp['parameters'].apply(str)
        assert (len(all_ml_p) == len(tmp.drop_duplicates()))

        if (len(all_ml_p) > 0):
            logger.info(str(len(all_ml_p)) + ' ml-parameter options loaded')
            logger.info('get_all_ml_p() algorithms:' +
                        str(all_ml_p.algorithm.unique()))
        else:
            logger.error('get_all_ml_p() parsed no results')

        return all_ml_p
    # -----------------
    # Init methods
    # -----------------

    def initilize_recommenders(self, rec_class):
        """
        Initilize recommender
        """
        # default supervised learning recommender settings

        self.DEFAULT_REC_ARGS = {'metric': self.metric_}
        # if self.random_state:
        #self.DEFAULT_REC_ARGS['random_state'] = self.random_state

        # add static_parameters for each ML methods
        self.static_parameters = {}
        # set the registered ml parameters in the recommenders

        ml_p = self.get_all_ml_p()

        self.DEFAULT_REC_ARGS['ml_p'] = ml_p

        # Create supervised learning recommenders
        if self.rec_class is not None:
            self.rec_engines[self.mode] = self.rec_class(
                **self.DEFAULT_REC_ARGS)
        else:
            self.rec_engines[self.mode] = RandomRecommender(
                **self.DEFAULT_REC_ARGS)

        assert ml_p is not None
        assert len(ml_p) > 0

        logger.debug("recomendation engines initilized: ")
        for prob_type, rec in self.rec_engines.items():
            logger.debug(f'\tproblemType: {prob_type} - {rec}')
            logger.debug('\trec.ml_p:\n' + str(rec.ml_p.head()))

    def load_kb(self):
        """Bootstrap the recommenders with the knowledgebase."""
        logger.info('loading pmlb knowledgebase')

        kb = load_knowledgebase(
            resultsFiles=[self.knowledgebase],
            metafeaturesFiles=[self.kb_metafeatures]
        )

        # replace algorithm names with their ids
        #self.ml_name_to_id = {v:k for k,v in self.ml_id_to_name.items()}
        # kb['resultsData']['algorithm'] = kb['resultsData']['algorithm'].apply(
        #                                  lambda x: self.ml_name_to_id[x])

        all_df_mf = kb['metafeaturesData'].set_index('_id', drop=False)

        # all_df_mf = pd.DataFrame.from_records(metafeatures).transpose()
        # keep only metafeatures with results
        df = all_df_mf.loc[kb['resultsData'][self.mode]['_id'].unique()]
        self.dataset_mf_cache = self.dataset_mf_cache.append(df)
        # self.update_dataset_mf(kb['resultsData'])

        self.rec_engines[self.mode].update(
            kb['resultsData'][self.mode], self.dataset_mf_cache, source='knowledgebase')
        logger.info('Knowledgebase loaded')
        return kb['resultsData'][self.mode]

    # -----------------
    # Utility methods
    # -----------------

    # todo ! to working yet

    def get_results_metafeatures(self):
        """
        Return a pandas dataframe of metafeatures

        Retireves metafeatures from self.dataset_mf_cache if they exist,
        otherwise queries the api and updates the cache.

        :param results_data: experiment results with associated datasets

        """

        d = self.datasetId
        df = self.meta_features
        df['dataset'] = d
        df.set_index('dataset', inplace=True)
        self.dataset_mf_cache = self.dataset_mf_cache.append(df)

        return df

    def update_recommender(self, new_results_df):
        """Update recommender models based on new experiment results in
        new_results_df.
        """
        if len(new_results_df) >= 1:
            new_mf = self.get_results_metafeatures()
            self.rec_engines[self.mode].update(new_results_df, new_mf)
            logger.info(time.strftime("%Y %I:%M:%S %p %Z", time.localtime()) +
                        ': recommender updated')

    # -----------------
    # Syncronous actions an AI request can take
    # -----------------
    def generate_recommendations(self):
        """

        :returns list of maps that represent request payload objects
        """
        logger.info(
            "generate_recommendations({},{})".format(
                self.datasetId, self.n_recs_))

        recommendations = []

        #  metafeature need to generate from independent codes # todo

        #metafeatures = self.labApi.get_metafeatures(datasetId)

        # key code for generate recomendation need call this line or this
        # function into fit
        ml, p, ai_scores = self.rec_engines[self.mode].recommend(
            dataset_id=self.datasetId,
            n_recs=self.n_recs_,
            dataset_mf=self.meta_features)

        for alg, params, score in zip(ml, p, ai_scores):
            # TODO: just return dictionaries of parameters from rec
            # modified_params = eval(params) # turn params into a dictionary

            recommendations.append({'dataset_id': self.datasetId,
                                    'algorithm': alg,
                                    'parameters': params,
                                    'ai_score': score,
                                    })

        return recommendations

    def _stop_by_max_time_mins(self):
        """Stop optimization process once maximum minutes have elapsed."""
        if self.max_time_mins:
            total_mins_elapsed = (
                datetime.now() - self._start_datetime).total_seconds() / 60.
            return total_mins_elapsed >= self.max_time_mins
        else:
            return False

    def fit(self, X, y):
        """Trains PennAI on X,y.

        initialize: train recommender or load saved recommender state
        until stop criterion is met:
            get recommendations for X,y
            fit and cross validate recommended ML configs
            update recommender based on CV scores
        finalize: store best model, or make ensemble of trained models
            that meet some performance threshold

        """

        self.fit_init_()
        if self.random_state is not None:
            random.seed(self.random_state)
            np.random.seed(self.random_state)

        # generate datasetId based on import X, y
        # make pd.DataFrameBased on X, y
        if isinstance(X, np.ndarray):
            columns = ["Feature_{}".format(i) for i in range(X.shape[1])]
            features = pd.DataFrame(X, columns=columns)
        if "pennai_target" in features.columns:
            raise ValueError(
                'The column name "pennai_target" is not allowed in X, '
                'please check your dataset and remove/rename that column')

        # get meta_features based on X, y
        self.meta_features = self.generate_metafeatures_from_X_y(features, y)
        # save all results
        self.recomms = []

        for i, x in enumerate(self.algorithms):
            logger.debug('Importing ML methods: ' + str(x['name']))
            # import scikit obj from string
            exec('from {} import {}'.format(x['path'], x['name']))
        self._start_datetime = datetime.now()
        for i in range(self.n_iters):
            # stop by max_time if step
            if_stop = self._stop_by_max_time_mins()
            if if_stop:
                logger.info(
                    "Stop optimization process once"
                    " {} minutes have elapsed.".format(
                        self.max_time_mins))
                break

            logger.info("Start iteration #{}".format(i + 1))
            recommendations = self.generate_recommendations()
            new_results = []
            ests = []
            ress = []

            for r in recommendations:
                logger.debug(r)
                # evaluate each recomendation
                # convert string to scikit-learn obj
                est = eval(r['algorithm'])()

                # convert str to bool/none
                params = r['parameters']
                for k, v in params.items():
                    if isinstance(v, str):
                        new_v = bool_or_none(v)
                        params[k] = new_v
                # add staticparameters
                params.update(self.static_parameters[r['algorithm']])
                avail_params = est.get_params()

                if 'random_state' in avail_params and self.random_state:
                    params['random_state'] = self.random_state

                est.set_params(**params)
                # initilize a result
                res = {
                    '_id': self.datasetId,
                    'algorithm': r['algorithm'],
                    'parameters': params,
                }
                ests.append(est)
                ress.append(res)
            # Parallel computing step
            scores_list = Parallel(n_jobs=self.n_jobs)(delayed(
                cross_val_score)(estimator=est,
                                 X=X,
                                 y=y,
                                 cv=10,
                                 scoring=self.scoring_)
                for est in ests)
            # summary result
            for res, scores in zip(ress, scores_list):
                res[self.metric_] = np.mean(scores)
                new_results.append(res)

            self.recomms += new_results

            new_results_df = pd.DataFrame(new_results)
            # get best score
            best_score_iter = new_results_df[self.metric_].max()
            # update recommender each iteration
            self.update_recommender(new_results_df)
            # get best score in new results in this iteration
            # todo for early stop termination

        # convert to pandas.DataFrame from finalize result
        self.recomms = pd.DataFrame(self.recomms)
        self.recomms.sort_values(
            by=self.metric_,
            ascending=False,
            inplace=True
        )
        self.best_result_score = self.recomms[self.metric_].values[0]
        self.best_result = self.recomms.iloc[0]
        self.best_algorithm = self.best_result['algorithm']
        self.best_params = self.best_result['parameters']

        if not self.ensemble:
            self.estimator = eval(self.best_algorithm)()
            self.estimator.set_params(**self.best_params)
        else:
            ensemble_ests = self.recomms['algorithm'].values[:self.ensemble]
            ests_params = self.recomms['parameters'].values[:self.ensemble]
            estimators = []
            for est, params in zip(ensemble_ests, ests_params):
                estimator = eval(est)()
                estimator.set_params(**params)
                est_name = 'clf' + str(len(estimators))
                estimators.append((est_name, estimator))
            if self.mode == "classification":
                self.estimator = VotingClassifier(estimators=estimators,
                                                  voting='hard',
                                                  n_jobs=self.n_jobs)
            else:
                self.estimator = VotingRegressor(estimators=estimators,
                                                 voting='hard',
                                                 n_jobs=self.n_jobs)

        self.estimator.fit(X, y)
        logger.info("Best model: {}".format(self.estimator))

        return self

    def predict(self, X):
        """Predict using trained model."""
        if not hasattr(self, 'estimator'):
            raise RuntimeError(
                'A estimator has not yet been optimized.'
                ' Please call fit() first.'
                )
        return self.estimator.predict(X)

    def score(self, X, y):
        """Return the score on the given testing data using the user-specified
        scoring function.
        Parameters
        ----------
        X: array-like {n_samples, n_features}
            Feature matrix of the testing set
        y: array-like {n_samples}
            List of class labels for prediction in the testing set
        Returns
        -------
        accuracy_score: float
            The estimated test set accuracy
        """
        if not hasattr(self, 'estimator'):
            raise RuntimeError(
                'A estimator has not yet been optimized.'
                ' Please call fit() first.'
                )
        scorer = SCORERS[self.scoring_]
        score = scorer(
            self.estimator,
            X,
            y
        )
        return score

    def save(self, filename):
        """save pickled recommender.
        Parameters
        ----------
        filename: string
            Filename for saving pickled recommender.

        Returns
        -------
        None
        """
        self.rec_engines[self.mode].save(filename)


def bool_or_none(val):
    """Convert string to boolean type/None.
    Parameters
    ----------
    val: string
        Value of a parameter in string type

    Returns
    -------
    _: boolean or None
        Converted value in boolean type
    """
    if (val.lower() == 'true'):
        return True
    elif (val.lower() == 'false'):
        return False
    elif (val.lower() == 'none'):
        return None
    else:
        return val


class PennAIClassifier(PennAI, ClassifierMixin):
    mode = "classification"
    scoring_ = "accuracy"


class PennAIRegressor(PennAI, RegressorMixin):
    mode = "regression"
    scoring_ = "neg_mean_squared_error"
