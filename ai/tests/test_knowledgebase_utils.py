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


import ai.knowledgebase_utils as kb_utils
import unittest
from unittest import skip
from unittest.mock import Mock, patch
from nose.tools import (nottest, raises, assert_equals,
        assert_is_instance, assert_dict_equal)
from parameterized import parameterized
import pandas as pd
import pprint
import math

TEST_OUTPUT_PATH = "target/test_output/test_knowledgebase_utils"

@nottest
def isClose(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''
    https://www.python.org/dev/peps/pep-0485/#proposed-implementation
    '''
    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        #print(f"not floats: '{a}', '{b}'")
        return a == b

    ##if not(abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)):
    ##    print(f"tol check failed: {a}, {b}, {max(rel_tol * max(abs(a),
    ##      abs(b)), abs_tol)}, {abs(a-b)}")

    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

@nottest
def load_test_data():
    '''
    testName
    resultsFiles
    datasetDirectory
    jsonMetafeatureDirectory
    metafeaturesFiles
    targetField
    expectedResultsCount
    expectedMetafeaturesCount
    expectedWarningCount
    '''
    return [
        ("benchmark6-metafeaturesFromDirectory",
         ["data/knowledgebases/"
             "sklearn-benchmark-data-knowledgebase-r6-small.tsv.gz"],
         'data/knowledgebases/test/jsonmetafeatures',
         '',
         'class',
         155, # this corresponds to the number of results from datasets w mf
         5,
         1
         ),
        ("benchmark6-classification_metafeaturesFromFile",
         ["data/knowledgebases/"
             "sklearn-benchmark-data-knowledgebase-r6-small.tsv.gz"],
         '',
         ['data/knowledgebases/pmlb_classification_metafeatures.csv.gz'],
         'class',
         5226,
         164,
         0
         ),
        ("benchmark-regression_metafeaturesFromFile",
         ["data/knowledgebases/"
             "pmlb_regression_results-small.tsv.gz"],
         '',
         ['data/knowledgebases/pmlb_regression_metafeatures.csv.gz'],
         'target',
         100,
         65,
         0
         ),
        ("multiResultFile-metafeaturesFromFile",
         [("data/knowledgebases/test/results/"
             "sklearn-benchmark5-data-knowledgebase_filtered1.tsv"),
            ("data/knowledgebases/test/results/"
            "sklearn-benchmark5-data-knowledgebase_filtered2.tsv")],
         '',
         ['data/knowledgebases/pmlb_classification_metafeatures.csv.gz'],
         'class',
         6,
         1,
         0
         ),
        ("benchmark6-metafeaturesFromMultiFile",
         ["data/knowledgebases/"
             "sklearn-benchmark-data-knowledgebase-r6-small.tsv.gz"],
         '',
         ['data/knowledgebases/test/metafeatures/pmlb_metafeatures1.csv',
            'data/knowledgebases/test/metafeatures/pmlb_metafeatures2.csv'],
         'class',
         5226,
         164,
         0
         ),
    ]

def load_default_kb_data():
    # /test/results contains dupes from pmlb
    return [
        ("pmlbOnly", True, None, None, 1519785, 284),
        ("userOnly", False, "data/knowledgebases/test/results",
            "data/knowledgebases/test/metafeatures", 6, 1),
        ("pmlbAndUser", True, "data/knowledgebases/test/results",
            "data/knowledgebases/test/metafeatures", 1519786, 284)
    ]

def results_files():
    return [
    (   "benchmark6",
        "data/knowledgebases/"
        "sklearn-benchmark-data-knowledgebase-r6-small.tsv.gz"),
    (   "test1",
        "data/knowledgebases/test/results/"
        "sklearn-benchmark5-data-knowledgebase_filtered1.tsv"),
    (   "test2",
        "data/knowledgebases/test/results/"
        "sklearn-benchmark5-data-knowledgebase_filtered2.tsv"),
    (   "test3 pickle",
        "data/knowledgebases/"
        "sklearn-benchmark5-data-knowledgebase-small.pkl.gz"),
    (   "test4 json",
        "data/knowledgebases/"
        "sklearn-benchmark5-data-knowledgebase-small.json.gz"),
    ]

def dupe_results_data():
    #columns, data, originalShape, dedupeShape
    return [

        (
            ["parameters", "r2_cv_mean", "explained_variance_cv_mean", "neg_mean_squared_error_cv_mean",
             "neg_mean_absolute_error_cv_mean", "time", "seed", "dataset", "algorithm", "_id"],

            [
                [{'alpha': 0.9, 'criterion': 'friedman_mse', 'init': None}, 0.1992009361802493, 0.23368152052158514, -0.7399201059000751, -0.6496514345462184,
                 0.033953523635864256, 24800, "658_fri_c3_250_25", "GradientBoostingRegressor", "68203b2f4c735c5c6c510719a2b02ce0d8138457cccc8015d0479c297906bbdf"],
                [{'C': 0.0001, 'cache_size': 700, 'coef0': 10, 'degree': 2}, -0.2871841075837208, 7.206677874449507e-06, -9544.785895105535, -70.89032992668359,
                 0.0009400367736816408, 24800, "706_sleuth_case1202", "SVR", "9f587c3497db3e74321d0bbc9cbf051af08552f665262f736665f338809582ee"],
                [{'criterion': 'mse', 'max_depth': 5, 'max_features': None}, 0.10941330863886542, 0.1255369211644101, -0.873978489465834, -0.7157552225552044,
                 0.0013549327850341795, 24800, "623_fri_c4_1000_10", "DecisionTreeRegressor", "c4991f7f7db210de7f3439643c94f0e4db1589478dedda01c3fea698ed6b1c96"],
                [{'max_depth': 5, 'criterion': 'mse', 'max_features': None}, 0.10941330863886542, 0.1255369211644101, -0.873978489465834, -0.7157552225552044,
                 0.0013549327850341795, 24800, "623_fri_c4_1000_10", "DecisionTreeRegressor", "c4991f7f7db210de7f3439643c94f0e4db1589478dedda01c3fea698ed6b1c96"],
                [{'C': 0.01, 'cache_size': 700, 'coef0': 0.0, 'degree': 2}, -0.07517126969691883, 1.7985612998927535e-15, -20.307712846815406, -
                 3.6415499898232495, 0.003330850601196289, 24800, "229_pwLinear", "SVR", "b84b30823e3a0b65441d703d4fd1a1e45535cb2e976590a7e8379db6a187ab38"],
                [{'cache_size': 700, 'C': 0.01, 'coef0': 0.0, 'degree': 2}, -0.07517126969691883, 1.7985612998927535e-15, -20.307712846815406, -
                 3.6415499898232495, 0.003330850601196289, 24800, "229_pwLinear", "SVR", "b84b30823e3a0b65441d703d4fd1a1e45535cb2e976590a7e8379db6a187ab38"],
            ],
            (6, 10),
            (4, 10)
        )
    ]


class TestResultUtils(unittest.TestCase):

    def check_result(self, result, expectedResultsCount=0,
            expectedMetafeaturesCount=0, expectedWarningCount=0):
        """checks results of load_knowledgebase calls with expectations"""

        assert 'resultsData' in result
        assert 'metafeaturesData' in result

        assert isinstance(result['resultsData'], dict)
        total_results = 0
        for v in result['resultsData'].values():
            assert isinstance(v, pd.DataFrame)
            self.assertGreater(len(v), 0)
            total_results+= len(v)

        self.assertEquals(total_results, expectedResultsCount)

        assert isinstance(result['metafeaturesData'], pd.DataFrame)

        print(f"found {len(result['warnings'])} result.warnings:")
        print("\n".join(result['warnings']))

        self.assertEquals(len(result['warnings']), expectedWarningCount,
                msg = f"warnings: {result['warnings']}")

        self.assertEquals(len(result['metafeaturesData']),
                expectedMetafeaturesCount)

    @parameterized.expand(load_test_data)
    def test_load_knowledgebase(self, testName, resultsFiles,
        jsonMetafeatureDirectory, metafeaturesFiles, targetField,
        expectedResultsCount, expectedMetafeaturesCount, expectedWarningCount):

        result = kb_utils.load_knowledgebase(
            resultsFiles=resultsFiles,
            metafeaturesFiles=metafeaturesFiles,
            jsonMetafeatureDirectory=jsonMetafeatureDirectory)

        print('expectedResultsCount',expectedResultsCount)
        print('expectedWarningCount',expectedWarningCount)
        print('expectedMetafeaturesCount',expectedMetafeaturesCount)
        self.check_result(result,
                expectedResultsCount=expectedResultsCount,
                expectedMetafeaturesCount=expectedMetafeaturesCount,
                expectedWarningCount=expectedWarningCount)
        # assert 'resultsData' in result
        # assert 'metafeaturesData' in result

        # assert isinstance(result['resultsData'], dict)
        # for v in result['resultsData'].values():
        #     assert isinstance(v, pd.DataFrame)
        #     self.assertGreater(len(v), 1)
        # assert isinstance(result['metafeaturesData'], pd.DataFrame)

        # self.assertGreater(len(result['metafeaturesData']), 1)

        # print(f"test_load_knowledgebase found "
        #     f"{len(result['warnings'])} result.warnings:")
        # print("\n".join(result['warnings']))

        # self.assertEquals(len(result['warnings']), expectedWarningCount,
        #         msg = f"warnings: {result['warnings']}")

        # self.assertEquals(len(result['metafeaturesData']),
        #         expectedMetafeaturesCount)
        # self.assertEquals(len(result['resultsData']), expectedResultsCount)


    @parameterized.expand(results_files)
    def test_load_results_from_file(self, name, testResultsFiles):
        data = kb_utils._load_results_from_file(testResultsFiles)
        assert isinstance(data, pd.DataFrame)

        self.assertGreater(len(data), 1)
        #assert expectedResultsData.equals(data)

    def test_generate_metadata_from_directory(self):
        testResultsDataDirectory = "data/datasets/pmlb_small"
        targetField = "class"
        prediction_type = "classification"

        data = kb_utils._generate_metadata_from_directory(
                testResultsDataDirectory,
                prediction_type=prediction_type,
                targetField=targetField)
        assert isinstance(data, dict)

        self.assertGreater(len(data.keys()), 1)
        #assert expectedMetafeaturesData.equals(data)

    @parameterized.expand(load_default_kb_data)
    def test_load_default_knowledgebases(self, name, usePmlb,
            userKbResultsPath, userKbMetafeaturesPath,
            expectedResultsCount, expectedMetafeaturesCount):
        """the PMLB knowledgebase is loaded correctly"""
        result = kb_utils.load_default_knowledgebases(
            usePmlb=usePmlb,
            userKbResultsPath=userKbResultsPath,
            userKbMetafeaturesPath=userKbMetafeaturesPath
            )

        self.check_result(result,
                expectedResultsCount=expectedResultsCount,
                expectedMetafeaturesCount=expectedMetafeaturesCount
                )
        # assert 'resultsData' in result
        # assert 'metafeaturesData' in result

        # assert isinstance(result['resultsData'], pd.DataFrame)
        # assert isinstance(result['metafeaturesData'], pd.DataFrame)

        # self.assertEquals(len(result['resultsData']),
        #         expectedResultsCount)
        # self.assertEquals(len(result['metafeaturesData']),
        #         expectedMetafeaturesCount)

        # print(f"test_load_default_knowledgebases found "
        #     f"{len(result['warnings'])} result.warnings:")
        # print("\n".join(result['warnings']))

        # assert len(result['warnings']) == 0


    def test_load_json_metafeatures_from_directory(self):
        testDirectory = "data/knowledgebases/test/jsonmetafeatures"
        testDatasets = ["adult", "agaricus-lepiota", "allbp", "allhyper",
                "allhypo"]

        result = kb_utils._load_json_metafeatures_from_directory(
                testDirectory, testDatasets)
        assert len(result) == len(testDatasets)

        for dataset in testDatasets:
            assert dataset in result.keys()

    def test_load_metafeatures_from_file(self):
        pmlbMetafeaturesFile = \
                "data/knowledgebases/pmlb_classification_metafeatures.csv.gz"
        result = kb_utils._load_metadata_from_file(pmlbMetafeaturesFile)
        assert len(result) == 165

    def test_generate_metafeatures_file(self):
        datasetDirectory = "data/datasets/pmlb_small"
        outputFilename = 'metafeatures.csv.gz'
        targetField = 'class'
        predictionType = "classification"

        mfGen = kb_utils.generate_metafeatures_file(
            outputFilename=outputFilename,
            outputPath=TEST_OUTPUT_PATH,
            datasetDirectory=datasetDirectory,
            fileExtensions = ['.csv', '.tsv', '.gz'],
            targetField = targetField,
            checkSubdirectories = True)

        assert len(mfGen) > 10

        mfLoad = kb_utils._load_metadata_from_file(
                f"{TEST_OUTPUT_PATH}/{outputFilename}")

        self.assertIsInstance(mfGen, dict)
        self.assertIsInstance(mfLoad, dict)

        #assert that mfLoad and mfGen are equal
        self.assert_metafeature_dict_equality(mfGen, mfLoad)

    @parameterized.expand(dupe_results_data)
    def test_dedupe_results_dataframe(self, columns, data, originalShape, dedupeShape):
        df = pd.DataFrame(data, columns = columns)

        self.assertEquals(df.shape, originalShape)
        kb_utils.dedupe_results_dataframe(df)
        self.assertEquals(df.shape, dedupeShape)


    def assert_metafeature_dict_equality(self, mf1, mf2):
        '''
        assert that two metafeature dictionaries are equal

        cannot do direct dict equalty because:
            - metafeatures loaded from file are of type <str:Dict>,
            metafeatures loaded generated are of type <str:OrderedDict>
            - can contain nan values which are not equal in python
        '''
        tolerance = 0
        #tolerance = 0.0000000000001
        mutualKeys = set(mf1.keys()) & set(mf2.keys())

        for key in mutualKeys:
            for field in mf1[key].keys():
                gen = mf1[key][field]
                load = mf2[key][field]
                #print(f"{key}:{field}  {type(gen)}:{type(load)}  {gen}:{load}")
                self.assertTrue(
                    #(gen == load) or
                    isClose(gen, load, abs_tol=tolerance)
                    or ((gen==None or math.isnan(gen))
                        and (load==None or math.isnan(load))),
                    msg= (f"For key/field '{key}'/'{field}', values not equal:"
                        " {type(gen)}:{type(load)}  '{gen}':'{load}'"))

        self.assertEqual(set(mf1.keys()), set(mf2.keys()))
