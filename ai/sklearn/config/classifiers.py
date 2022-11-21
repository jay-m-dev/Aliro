classifier_config_dict = {

    # Original six classifiers
    'sklearn.tree.DecisionTreeClassifier': {
        'params': {
            'criterion': ["gini", "entropy"],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 5, 10, 20],
            'min_weight_fraction_leaf': [0.0, 0.05, 0.1, 0.15, 0.2,  0.25, 0.3, 0.35, 0.4, 0.45],
            'max_features': ["sqrt", "log2", None]
        }

    },

    'sklearn.ensemble.GradientBoostingClassifier': {
        'params': {
            'n_estimators': [100, 500],
            'learning_rate': [0.01, 0.1, 1],
            'max_depth': [1, 3, 5, 10],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 5, 10, 20],
            'subsample': [0.5, 1],
            'max_features': ["sqrt", "log2"]
        }
    },

    'sklearn.neighbors.KNeighborsClassifier': {
        'params': {
            'n_neighbors': [1, 3, 5, 7, 9, 11],
            'weights': ["uniform", "distance"],
            'p': [1, 2]
        },
    },

    'sklearn.svm.SVC': {
        'params': {
            'kernel': ["poly", "rbf"],
            'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
            'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
            'gamma': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
            'degree': [2, 3],
            'coef0': [0.0, 0.0001, 0.001, 0.01, 0.1, 1, 10]
        },
        'static_parameters': {
            'cache_size': 700, # static_parameters
            'max_iter': 10000, # static_parameters
            'probability': True, # static_parameters
        }
    },

    'sklearn.linear_model.LogisticRegression': {
        'params': {
            'penalty': ["l1", "l2"],
            'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
            'dual': [True, False],
            'fit_intercept': [True, False]
        },
        'static_parameters': {
            'solver': "liblinear",
            'multi_class': "auto",
        },
        #invalidParameterCombinations
        "invalid_params_comb" : [
            [{"penalty":"l1"}, {"dual": True}]
        ]
    },

    'sklearn.ensemble.RandomForestClassifier': {
        'params': {
            'n_estimators': [100, 500],
            'criterion': ["gini", "entropy"],
            'max_features': ["sqrt", "log2", None],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf':  [1, 5, 10, 20],
            'bootstrap': [True, False],
            'min_weight_fraction_leaf': [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
        }
    },





    # new classifiers
    # 'sklearn.ensemble.AdaBoostClassifier': {
    #     'params': {
    #         'n_estimators': [100, 500],
    #         'learning_rate': [0.01, 0.1, 1],
    #         'algorithm': ["SAMME", "SAMME.R"]
    #     }
    # },

    
    # 'sklearn.cluster.KMeans': {
    #     'params': {
    #         'n_clusters': [2, 3, 4, 5, 6, 7, 8, 9, 10],
    #         'init': ["k-means++", "random"],
    #         'n_init': [10, 20, 30],
    #         'max_iter': [100, 200, 300, 400, 500],
    #         'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    #     }
    # },

    # 'sklearn.naive_bayes.GaussianNB': {
    #     'params': {
    #         'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    #     }
    # },

    # 'sklearn.naive_bayes.MultinomialNB': {
    #     'params': {
    #         'alpha': [0.0, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
    #         'fit_prior': [True, False]
    #     }
    # },

    # 'sklearn.naive_bayes.BernoulliNB': {
    #     'params': {
    #         'alpha': [0.0, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
    #         'fit_prior': [True, False]
    #     }
    # },

    # 'sklearn.neural_network.MLPClassifier': {
    #     'params': {
    #         'hidden_layer_sizes': [(100,), (100, 100), (100, 100, 100)],
    #         'activation': ["identity", "logistic", "tanh", "relu"],
    #         'solver': ["lbfgs", "sgd", "adam"],
    #         'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
    #         'learning_rate': ["constant", "invscaling", "adaptive"],
    #         'learning_rate_init': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
    #         'power_t': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    #         'max_iter': [100, 500, 1000, 2000, 5000, 10000],
    #         'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
    #         'momentum': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    #         'nesterovs_momentum': [True, False],
    #         'early_stopping': [True, False],
    #         'beta_1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    #         'beta_2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    #         'epsilon': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
    #         'validation_fraction': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    #         'n_iter_no_change': [5, 10, 20, 50, 100]
    #     }
    # }



}
