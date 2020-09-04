"""~This file is part of the PennAI library~

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

"""
"""
API utility functions for Penn-AI
"""

import pandas as pd
import numpy as np
import pdb
import simplejson as json
import requests
import itertools as it
import logging
import sys
from enum import Enum, auto, unique
from sklearn.model_selection import ParameterGrid # utility for hyperparams


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(module)s: %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

@unique
class AI_STATUS(Enum):
    ON = "on"
    OFF = "off"
    FINISHED = "finished"
    REQUESTED = "requested"

@unique
class RECOMMENDER_STATUS(Enum):
    DISABLED = 'disabled'
    INITIALIZING = 'initializing'
    RUNNING = 'running'

class LabApi:
    """Class for communicating with the PennAI server
    """

    def __init__(self, api_path, user, api_key, extra_payload, verbose):
        """
        :param api_path: string - path to the lab api server
        :param extra_payload: dict - any additional payload that needs to be
            specified
        :param api_key: string -
        :param user: string - test user
        :param verbose: Boolean
        """
        self.api_path = api_path
        self.exp_path = '/'.join([self.api_path,'api/experiments'])

        self.projects_path = '/'.join([self.api_path,'api/v1/projects'])
        self.algo_path = '/'.join([self.api_path,'api/projects'])

        self.data_path = '/'.join([self.api_path,'api/datasets'])
        self.status_path = '/'.join([self.api_path,'api/v1/datasets'])
        self.submit_path = '/'.join([self.api_path,'api/userdatasets'])

        self.recommender_path = '/'.join([self.api_path,'api/recommender'])
        
        self.api_key=api_key
        self.user=user
        self.verbose=False
        self.header = {'content-type': 'application/json'}
        # optional extra payloads (e.g. user id) for posting to the api
        self.extra_payload = extra_payload
        # static payload is the payload that is constant for every API post
        # with api key for this host
        self.static_payload = {'apikey':self.api_key}
        # add any extra payload
        self.static_payload.update(extra_payload)


        logger.debug("==LabApi paths:")
        logger.debug("self.api_path: " + self.api_path)

        logger.debug("self.exp_path: " + self.exp_path)

        logger.debug("self.projects_path: " + self.projects_path)
        logger.debug("self.algo_path: " + self.algo_path)

        logger.debug("self.data_path: " + self.data_path)
        logger.debug("self.status_path: " + self.status_path)
        logger.debug("self.submit_path: " + self.submit_path)

        logger.debug("self.recommender_path: " + self.recommender_path)
     
    def set_recommender_status(self, status):
        """Attempt to set the recommender status

        :param status 
        """
        logger.info("set_recommender_status(" + str(status) + ")")

        payload = {'status':status}
        data_submit_path = '/'.join([self.recommender_path, "status"])
        res = self.__request(path=data_submit_path, payload=payload, method="POST")

        data = json.loads(res.text)
        return data

    def launch_experiment(self, algorithmId, payload):
        """Attempt to start a ml experiment.

        :param algorithmId: string -
        :param payload: dict - dictionary describing the ml experiment parameters

        :returns: dict {value(str): status(str)}
        """
        logger.info("launch_experiment(" + str(algorithmId) + ", " + str(payload))
        assert algorithmId
        rec_path = '/'.join([self.projects_path, algorithmId, 'experiment'])

        # 503 code is returned if no capactiy available
        # This is a valid scenario and should not cause an exception
        res = self.__request(path=rec_path, payload=payload,
            headers=self.header,
            acceptableNotOkStatusCodes=[503])

        submitResponses = json.loads(res.text)

        #parse json response into named array
        submitStatus={}
        if len(submitResponses) > 0:
            for submitI in submitResponses:
                submitStatus[submitI] = submitResponses[submitI]

        return submitStatus

    def get_projects(self):
        """Get the descriptions and parameters of the supported ml algorithms

        :return: dict - algorithm descriptions as returned by api/projects
        """
        logger.info("get_projects()")

        res = self.__request(path=self.projects_path)
        data = json.loads(res.text)
        return data


    def get_filtered_datasets(self, payload):
        """Get datasets with filters

        :param payload: dict
            How to filter the results {'ai':['requested','finished']}

        :return: dict
            datasets that pass the payload filter
        """
        logger.info("get_filtered_datasets()")

        res = self.__request(path=self.data_path, payload=payload)
        data = json.loads(res.text)
        return data

    def get_dataset_ai_status(self, datasetId):
        """Get the ai status of a particular dataset
        """
        logger.info(f"get_dataset_ai_status('{datasetId}')")

        payload = {}
        path = '/'.join([self.data_path, datasetId])

        res = self.__request(path=path, payload=payload, method="GET")
        data = json.loads(res.text)
        data = data[0]

        #logger.debug(f"get_dataset_ai_status data: {data}")

        aiStatus = None
        if ("ai" in data):
            aiStatus = data["ai"]

        logger.info(f"get_dataset_ai_status('{datasetId}') = '{aiStatus}'")

        return aiStatus

    def get_new_experiments(self, last_update):
        """Get experiments that occurred after last_update

        :param last_update: int -

        :returns: dict - ml experiments results
        """
        logger.info("get_new_experiments(" + str(last_update)+ ")")

        payload = {'date_start':last_update,'has_scores':True}

        res = self.__request(path=self.exp_path, payload=payload)
        data = json.loads(res.text)
        return data

    def get_new_experiments_as_dataframe(self, last_update):
        """
        Get experiments that occured after last_update and return a dataframe

        :param last_update: int -

        :returns: dataframe - last experiments

        """
        logger.info("get_new_experiments_as_dataframe(" + str(last_update)+ ")")

        data = self.get_new_experiments(last_update)

        processed_data = []
        for d in data:
            if ('_options' in d.keys() and '_scores' in d.keys()
                and '_dataset_id' in d.keys()):
                frame={
                    'dataset_id':d['_dataset_id'],
                    'algorithm':d['_project_id'],
                    'parameters':d['_options'],
                    'prediction_type':d['_prediction_type'],
                }

                if(d['_prediction_type'] == "classification"):
                    #! This is balanced accuracy!
                    frame['accuracy'] = d['_scores']['accuracy_score']
                    frame['f1'] = d['_scores']['f1_score']

                elif(d['_prediction_type'] == "regression"):
                    frame['r2_cv_mean'] = d['_scores']['r2_score']
                else:
                    msg = (f'error in get_new_experiments_as_dataframe(), '
                            'experiment has unhandled _prediction_type '
                            f'{d["_prediction_type"]}')
                    raise RuntimeError(msg)
                new_experiment = pd.DataFrame([frame])
                assert not new_experiment.isna().any().any(), \
                        "Nan results in experiment"
                processed_data.append(frame)
            else:
              logger.error("new results are missing these fields:",
                      '_options' if '_options' not in d.keys() else '',
                      '_scores' if '_scores' not in d.keys() else '',
                      '_dataset_id' if '_dataset_id' not in d.keys() else '')

        new_experiments = pd.DataFrame(processed_data)

        return new_experiments

    def set_ai_status(self, datasetId, aiStatus):
        """set the ai status for the given dataset.

        :param datasetId: string - dataset to update
        :param aiStatus: string
        """
        logger.info("set_ai_status(" + str(datasetId) +", " + str(aiStatus) + ")")

        payload = {'ai':aiStatus}
        data_submit_path = '/'.join([self.submit_path, datasetId,'ai'])
        res = self.__request(path=data_submit_path, payload=payload, method="PUT")
        return res

    # @Deprecated, used in ai.py; redundant
    def get_ml_id_dict(self):
        """Returns a dictionary for converting algorithm IDs to names.

        :return: dict {mlId(str):mlName(str)}
        """
        logger.info("get_ml_id_dict()")

        res = self.__request(path=self.algo_path)
        responses = json.loads(res.text)

        ml_id_to_name = {}
        for ml in responses:
            ml_id_to_name.update({ml['_id']:ml['name']})

        return ml_id_to_name


    # @Deprecated, used in ai.py; redundant
    def get_user_datasets(self, user):
        """Returns a dictionary for converting dataset IDs to names.

        :return: dict {datasetId(str):datasetName(str)}
        """
        logger.info("get_user_datasets(" + str(user) + ")")

        payload = {'username':user}
        res = self.__request(path=self.submit_path, payload=payload)

        responses = json.loads(res.text)
        dataset_id_to_name = {}
        for dataset in responses:
            dataset_id_to_name.update({dataset['_id']:dataset['name']})
        return dataset_id_to_name


    def get_metafeatures(self, datasetId):
            """Fetches dataset metafeatures, returning dataframe.

            :param datasetId: dataset ID
            :return df: a dataframe of metafeatures, sorted by mf name
            """
            logger.info("get_metafeatures(" + str(datasetId) + ")")

            try:
                res = self.__request(path=self.data_path+'/'+datasetId,
                        method='GET')
                data = json.loads(res.text)

            except Exception as e:
                logger.error('exception when grabbing metafeature data for'
                        + str(datasetId))
                raise e

            data = data[0]
            mf = [data['metafeatures']]
            df = pd.DataFrame.from_records(mf,columns=mf[0].keys())
            print('api_utils:get_metafeatures')
            #include dataset name
            df['dataset'] = data['name']
            df.sort_index(axis=1, inplace=True)

            #logger.debug("metafeatures:")
            #logger.debug(df.head())

            return df

    def valid_combo(self, combo, bad_combos):
        """Checks if parameter combination is valid."""
        for bad_combo in bad_combos:
            bc = {}
            for b in bad_combo:
                bc.update(b)
            bad = True
            for k,v in bc.items():
                if combo[k] != v:
                    bad = False
        return not bad

    def get_all_ml_p(self, categoryFilter = None):
        """
        Returns a list of ml and parameter options for the user 'pennai'
        from the server.

        :returns: pd.DataFrame - unique ml algorithm and parameter combinations
            with columns 'alg_name', 'category', 'alg_name', 'parameters'
            'parameters' is a dictionary of parameters
        """
        logger.info("get_all_ml_p()")
        payload = {"username":"pennai"}

        # get the algorithm list for the user 'pennai'
        r = self.__request(path=self.api_path+'/api/preferences', payload=payload,
                method='GET')
        response = json.loads(r.text)

        if len(response) != 1:
            msg = 'error: get_all_ml_p() got ' + str(len(response))
            + ' user preferences, expected 1.'
            logger.error(msg)
            logger.error(response)
            raise RuntimeError(msg)

        if (response[0]['username'] != 'pennai'):
            msg = ('error: get_all_ml_p() did not get user "pennai", got "'
                    + str(response[0]['username']) + '"')
            logger.error(msg)
            logger.error(response)
            raise RuntimeError(msg)

        algorithms = response[0]['algorithms']
        logger.debug('response.algorithms length(): ' + str(len(algorithms)))

        if (categoryFilter):
            assert isinstance(categoryFilter, str)
            algorithms = [a for a in algorithms if a['category'] == categoryFilter]

        result = [] # returned value
        good_def = True # checks that json for ML is in good form

        for i,x in enumerate(algorithms):
            logger.debug('Checking ML: ' + str(x['name']))
            hyperparams = x['schema'].keys()
            hyperparam_dict = {}

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
                print(len(all_hyperparam_combos),'hyperparameter combinations for',
                        x['name'])

                for ahc in all_hyperparam_combos:
                    if 'invalidParameterCombinations' in x.keys():
                        if not self.valid_combo(ahc,
                                x['invalidParameterCombinations']):
                            continue
                    result.append({'algorithm':x['_id'],
                                   'category':x['category'],
                                   'parameters':ahc,
                                   'alg_name':x['name']})
            else:
                logger.error('warning: ' + str(x['name']) + 'was skipped')
            good_def = True


        # convert to dataframe, making sure there are no duplicates
        all_ml_p = pd.DataFrame(result)
        tmp = all_ml_p.copy()
        tmp['parameters'] = tmp['parameters'].apply(str)
        assert ( len(all_ml_p) == len(tmp.drop_duplicates()) )

        if (len(all_ml_p) > 0):
            logger.info(str(len(all_ml_p)) + ' ml-parameter options loaded')
            logger.info('get_all_ml_p() algorithms:' + str(all_ml_p.algorithm.unique()))
        else:
            logger.error('get_all_ml_p() parsed no results')

        return all_ml_p


    def __request(self, path, payload = None, method = 'POST',
            headers = {'content-type': 'application/json'},
            acceptableNotOkStatusCodes = []):
        """
        Attempt to make an api request and return the result.
        Throw an exception if the request fails or if a status code >400 is returned.

        :return: Requests.response object
        """

        logger.debug("Starting LabApi.__request(" + str(path) + ", " +
                str(payload) + ", " + str(method) + ", ...)" )

        if payload:
            assert isinstance(payload, dict)
            payload.update(self.static_payload)
        else:
            payload = self.static_payload

        res = None
        try:
            res = requests.request(method, path,
                    data=json.dumps(payload, ignore_nan=True),
                    headers=headers)
        except:
            logger.error("Unexpected error in LabApi.__request for path '" +
                    str(method) + ":" + str(path) + "':" + str(sys.exc_info()[0]))
            raise

        # check the status code
        if ((not res.ok)
            and (res.status_code not in acceptableNotOkStatusCodes)):
            msg = ("Request " + str(method) + " status_code not ok, path: '" +
                    str(path) + "' status code: '" + str(res.status_code) +
                    "'' response text: " + str(res.text))
            logger.error(msg)
            raise RuntimeError(msg)


        #logger.debug("Got response LabApi.__request(" + str(path) + ", ..., " + str(method) + ", ...)" )
        # try:
        #     logger.debug("response: ", str(res.text), "\n")
        # except:
        #     logger.debug("couldn't text parse response")
        return res
