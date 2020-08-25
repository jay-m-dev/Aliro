# Recommender system for Penn AI.
import pandas as pd
from pandas.util import hash_pandas_object
import hashlib
import os
import gzip
import pickle
import copy
# import json 
# import urllib.request, urllib.parse
from .base import BaseRecommender
#from ..metalearning import get_metafeatures
# from sklearn.preprocessing import RobustScaler 
# from sklearn.pipeline import Pipeline
import numpy as np
from collections import defaultdict, OrderedDict
import pdb
from surprise import (Reader, Dataset, CoClustering, SlopeOne, KNNWithMeans,
                      KNNBasic, mySVD) 
# import pyximport
# pyximport.install()
# from .svdedit import mySVD
from collections import defaultdict
import itertools as it
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(module)s: %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class SurpriseRecommender(BaseRecommender):
    """Class to support generic recommenders from the Surprise library.
    Not intended to be used as a standalone class. 

    Parameters
    ----------
    ml_type: str, 'classifier' or 'regressor'
        Recommending classifiers or regressors. Used to determine ML options.
    
    metric: str (default: accuracy for classifiers, mse for regressors)
        The metric by which to assess performance on the datasets.
    """
    def __init__(self, 
            ml_type='classifier', 
            metric=None, 
            ml_p=None,
            random_state=None, 
            knowledgebase_results=None,
            knowledgebase_metafeatures=None,
            load_serialized_rec="if_exists",
            serialized_rec_directory=None,
            serialized_rec_filename=None):

        """ set default recommender specific parameters; might be overwritten by loading serialized recommender"""
        if self.__class__.__name__ == 'SurpriseRecommender':
            raise RuntimeError('Do not instantiate the SurpriseRecommender class '
            'directly; use one of the method-specific classes instead.')
        self.set_algo()
        self.random_state = random_state
        if hasattr(self.algo, 'random_state'):
            self.algo.random_state = self.random_state
        # store results
        self.results_df = pd.DataFrame()
        self.first_fit = True 

        # reader for translating btw PennAI results and Suprise training set
        self.reader = Reader()

        self.ml_type = ml_type

        if metric is None:
            logger.debug('metric is None, setting...')
            self.metric='bal_accuracy' if self.ml_type=='classifier' else 'mse'
        else:
            self.metric = metric
        assert(self.metric is not None)

        logger.debug('self.algo_name: '+self.algo_name)
        logger.debug('ml_type: '+self.ml_type)
        logger.debug('metric: '+self.metric)
 
        self.min_epochs = 10
        self.max_epochs = 100

        """Initialize recommendation system."""
        super().__init__(
            ml_type, 
            metric, 
            ml_p, 
            serialized_rec_directory=serialized_rec_directory,
            serialized_rec_filename=serialized_rec_filename,
            load_serialized_rec=load_serialized_rec,
            knowledgebase_results=knowledgebase_results, 
            random_state=random_state)

    
    @property
    def algo_name(self):
        if type(self.algo).__name__ is None:
            return type(self).__name__
        return type(self.algo).__name__

    def _reconstruct_training_data(self, results_data, results_mf=None, 
            source='pennai'):
        """Used for loading pickled recomenders to set results_df 
        without training.
        :param results_data: DataFrame with columns corresponding to:
                'dataset'
                'algorithm'
                'parameters'
                self.metric
        :param results_mf: metafeatures for the datasets in results_data 
        :param source: str, optional (default: 'pennai')
            if 'pennai', will update tally of trained dataset models 
        """
        # update trained dataset models and hash table
        super().update(results_data, results_mf, source)
        # updates self.results_df and self.trainset
        self._update_training_data(results_data, shuffle=True)
        # check whether the set train data matches the pickled recommender's 
        # training data.
        rowHashes = hash_pandas_object(self.results_df).values 
        newHash = hashlib.sha256(rowHashes).hexdigest()
        if hasattr(self, 'results_df_hash'):
            if newHash == self.results_df_hash:
                logger.info('results_df hashes match')
            else:
                error_msg = 'the results_df hash from the pickle is different'
                logger.error(error_msg)
                raise ValueError(error_msg)
            del self.results_df_hash

    def load(self, filename=None, knowledgebase = None):
        """Load a saved recommender state."""
        if knowledgebase is None:
            logger.warning('A knowledgebase needs to be provided to load '
            'Surprise Recommenders from file. Not loading.')
            return 
        loaded = super().load(filename=filename)
        if loaded:
            logger.info('setting training data...')
            self._reconstruct_training_data(knowledgebase, 
                    source='knowledgebase')

    def save(self, filename=None):
        """Save the current recommender."""

        if filename is None:
            fn = self.serialized_rec_path
        else:
            fn = filename
        if os.path.isfile(fn):
            logger.warning('overwriting ' + fn)

        logger.info('saving recommender as ' + fn)
        f = gzip.open(fn, 'wb')
        save_dict = copy.deepcopy(self.__dict__)
        
        # remove results_df to save space. this gets loaded by load() fn.
        rowHashes = hash_pandas_object(save_dict['results_df']).values 
        save_dict['results_df_hash'] = hashlib.sha256(rowHashes).hexdigest() 
        logger.debug('save_dict[results_df]:'
                +str(save_dict['results_df'].head()))
        del save_dict['results_df']
        rowHashes = hash_pandas_object(save_dict['_ml_p'].apply(str)).values 
        save_dict['ml_p_hash'] = hashlib.sha256(rowHashes).hexdigest() 
        #del save_dict['_ml_p']
        del save_dict['mlp_combos']

        pickle.dump(save_dict, f, 2)
        f.close()

    def update(self, results_data, results_mf=None, source='pennai'):
        """Update ML / Parameter recommendations based on overall performance in 
        results_data.

        :param results_data: DataFrame with columns corresponding to:
                'dataset'
                'algorithm'
                'parameters'
                self.metric
        :param results_mf: metafeatures for the datasets in results_data 
        """

        # update trained dataset models and hash table
        super().update(results_data, results_mf, source)

        # update internal model
        self._update_model(results_data)

    def _update_training_data(self, results_data, shuffle=False):
        """Appends results_data to self.results_df. Sets the trainset for 
        the surprise recommender.
        
        :param results_data: DataFrame with columns corresponding to:
                'dataset'
                'algorithm'
                'parameters'
                self.metric
        :param shuffle: boolean, optional (default: False)
            If true, results_data is shuffled before it is added to 
            self.results_df or self.trainset.
        """

        if shuffle:
            # shuffle the results data 
            logger.debug('shuffling results_data')
            results_data = results_data.sample(frac=1, 
                    random_state=self.random_state)

        results_data.loc[:, 'algorithm-parameters'] =  (
                results_data['algorithm'].values + '|' +
                results_data['parameter_hash'].values)
        results_data.rename(columns={self.metric:'score'},inplace=True)
        logger.info('append and drop dupes')
        self.results_df = self.results_df.append(
                results_data[['algorithm-parameters','_id','score']]
                                                ).drop_duplicates()
        logger.info('load_from_df')
        data = Dataset.load_from_df(self.results_df[['_id', 
                                                     'algorithm-parameters', 
                                                     'score']], 
                                    self.reader, rating_scale=(0,1))
        # build training set from the data
        self.trainset = data.build_full_trainset()
        logger.debug('self.trainset # of ML-P combos: ' + 
                str(self.trainset.n_items))
        logger.debug('self.trainset # of datasets: ' 
                + str(self.trainset.n_users))

    def _update_model(self,results_data):
        """Stores new results and updates algo."""
        logger.debug('updating '+self.algo_name+' model')

        self._update_training_data(results_data, self.first_fit)
        self.first_fit=False

        logger.debug('fitting self.algo...')
        # set the number of training iterations proportionally to the amount of
        # results_data
        self.algo.fit(self.trainset)
        logger.debug('done.')
        logger.debug('model '+self.algo_name+' updated') 

    def recommend(self, dataset_id, n_recs=1, dataset_mf = None):
        """Return a model and parameter values expected to do best on dataset.

        Parameters
        ----------
        dataset_id: string
            ID of the dataset for which the recommender is generating 
            recommendations.
        n_recs: int (default: 1), optional
            Return a list of length n_recs in order of estimators and 
            parameters expected to do 
            best.
        """
        # dataset hash table
        super().recommend(dataset_id, n_recs, dataset_mf)
        # dataset_hash = self.dataset_id_to_hash[dataset_id]
        try:
            predictions = []
            filtered =0
            for alg_params in self.mlp_combos:
                if (dataset_id+'|'+alg_params not in 
                    self.trained_dataset_models):  
                    predictions.append(self.algo.predict(dataset_id, alg_params,
                                                         clip=False))
                else:
                    filtered +=1
            logger.debug('filtered '+ str(filtered) + ' recommendations')
            logger.debug('getting top n predictions') 
            ml_rec, phash_rec, score_rec = self._get_top_n(predictions, n_recs)
            logger.debug('returning ml recs') 
            
        except Exception as e:
            logger.error( 'error running self.best_model_prediction for'+
                    str(dataset_id))
            raise e 
        # update the recommender's memory with the new algorithm-parameter combos 
        # that it recommended
        self._update_trained_dataset_models_from_rec(dataset_id, 
                                                    ml_rec, phash_rec)

        p_rec = [self.hash_2_param[ph] for ph in phash_rec]
        return ml_rec, p_rec, score_rec

    def _get_top_n(self,predictions, n=10):
        '''Return the top-N recommendation for each user from a set of predictions.
        
        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.

        Returns:
            ml recs, parameter recs, and their scores in three lists
        '''

        # grabs the ml ids and their estimated scores for this dataset 
        top_n = [] 
        ml_dist = {}
        for uid, iid, true_r, est, _ in predictions:
            top_n.append((iid, est))
            ml = iid.split('|')[0]
            if ml in ml_dist.keys():
                ml_dist[ml] += 1.0
            else:
                ml_dist[ml] = 1.0
        n_ml = len(ml_dist.keys())

        ######
        # Shuffle top_n just to remove tied algorithm bias when sorting
        # Make uniform random choices from the Algorithms, then uniform random
        # choices from their parameters to shuffle top_n
        # the probability for each ML method is 1/total_methods/(# instances of that
        # method)
        inv_ml_dist = {k:1/n_ml/v for k,v in ml_dist.items()}
        top_n_dist = np.array([inv_ml_dist[tn[0].split('|')[0]] 
            for tn in top_n])
        top_n_idx = np.arange(len(top_n))
        top_n_idx_s = np.random.choice(top_n_idx, len(top_n), replace=False, 
                                       p=top_n_dist)
        top_n = [top_n[i] for i in top_n_idx_s]
        #####
        
        # sort top_n
        top_n = sorted(top_n, key=lambda x: x[1], reverse=True)
        top_n = top_n[:n]

        logger.debug('filtered top_n:'+str(top_n)) 
        ml_rec = [n[0].split('|')[0] for n in top_n]
        p_rec = [n[0].split('|')[1] for n in top_n]
        score_rec = [n[1] for n in top_n]
        return ml_rec, p_rec, score_rec 

class CoClusteringRecommender(SurpriseRecommender):
    """Generates recommendations via CoClustering, see
    https://surprise.readthedocs.io/en/stable/co_clustering.html
    """
    def set_algo(self):
        self.algo = CoClustering(n_cltr_u = 10)

    # def __init__(self, ml_type='classifier', metric=None, ml_p=None, 
    #         algo=None): 
    #     super().__init__(ml_type, metric, ml_p, algo)
    #     # set n clusters for ML equal to # of ML methods
    #     self.
    def _update_model(self,results_data):
        """Stores new results and updates algo."""
        self.algo.n_cltr_i = self.ml_p.algorithm.nunique()
        super()._update_model(results_data)

class KNNWithMeansRecommender(SurpriseRecommender):
    """Generates recommendations via KNNWithMeans, see
    https://surprise.readthedocs.io/en/stable/knn_inspired.html
    """
    def set_algo(self):
        self.algo = KNNWithMeans()

class KNNDatasetRecommender(SurpriseRecommender):
    """Generates recommendations via KNN with clusters defined over datasets, see
    https://surprise.readthedocs.io/en/stable/knn_inspired.html
    """
    def set_algo(self):
        self.algo = KNNBasic(sim_options={'user_based':True})

    @property
    def algo_name(self):
        return 'KNN-Dataset' 

class KNNMLRecommender(SurpriseRecommender):
    """Generates recommendations via KNN with clusters defined over algorithms, see
    https://surprise.readthedocs.io/en/stable/knn_inspired.html
    """
    def set_algo(self):
        self.algo = KNNBasic(sim_options={'user_based':False})
    @property
    def algo_name(self):
        return 'KNN-ML' 

class SlopeOneRecommender(SurpriseRecommender):
    """Generates recommendations via SlopeOne, see
    https://surprise.readthedocs.io/en/stable/slope_one.html
    """
    def set_algo(self):
        self.algo = SlopeOne()


class SVDRecommender(SurpriseRecommender):
    """SVD recommender.
    see https://surprise.readthedocs.io/en/stable/matrix_factorization.html 
    Recommends machine learning algorithms and parameters using the SVD algorithm.
        - stores ML + P and every dataset.
        - learns a matrix factorization on the non-missing data.
        - given a dataset, estimates the rankings of all ML+P and returns the top 
        n_recs. 

    Note that we use a custom online version of SVD found here:
    https://github.com/lacava/surprise
    """

    def set_algo(self, surprise_kwargs={}):
        alg_kwargs = {'n_factors':20, 
                'biased':True, 
                'init_mean':0,
                'init_std_dev':.2, 
                'lr_all':.01,
                'reg_all':.02,
                'verbose':'False'}
        alg_kwargs.update(surprise_kwargs)
        self.algo = mySVD(**alg_kwargs)

    # def __init__(self, ml_type='classifier', metric=None, ml_p=None, 
    #         filename=None, knowledgebase=None, random_state=None,
    #         surprise_kwargs={}): 
    #     super().__init__(ml_type=ml_type, metric=metric, ml_p=ml_p, 
    #             filename=filename, knowledgebase=knowledgebase, 
    #             random_state=random_state)
    
    def _update_model(self,results_data):
        """Stores new results and updates SVD."""
        logger.info('updating SVD model')
        # shuffle the results data the first time
        if self.first_fit:
            logger.debug('shuffling results_data')
            results_data = results_data.sample(frac=1, 
                    random_state=self.random_state)
            self.first_fit=False 

        self._update_training_data(results_data)
        # set the number of training iterations proportionally to the amount of
        # results_data
        logger.info('algo random_state: '+str(self.algo.random_state))
        self.algo.n_epochs = min(len(results_data),self.max_epochs)
        self.algo.n_epochs = max(self.algo.n_epochs,self.min_epochs)

        logger.debug('fitting self.algo...')
        self.algo.partial_fit(self.trainset)
        logger.debug('done.')
        logger.debug('model SVD updated') 
