"""~This file is part of the PennAI library~

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

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

def calculate_version():
    initpy = open('ai/_version.py').read().split('\n')
    version = list(filter(lambda x: '__version__' in x, initpy))[0].split('\'')[1]
    return version

package_version = calculate_version()

setup(
    name='pennaipy',
    version=package_version,
    author='Heather Williams, Weixuan Fu, William La Cava',
    author_email='hwilli@pennmedicine.upenn.edu, weixuanf@upenn.edu, lacava@upenn.edu',
    packages=find_packages(exclude=("tests",)),
    url='https://github.com/epistasislab/pennai',
    license='GNU/GPLv3',
    test_suite='nose.collector',
    tests_require=['nose'],
    description=('Penn Artificial Intelligence Data Assistant'),
    long_description='''
A system that intelligently manages machine learning workflows for data science

Contact: Heather Williams (hwilli@upenn.edu), Weixuan Fu (weixuanf@upenn.edu), William La Cava (lacava@upenn.edu)

This project is hosted at https://github.com/epistasislab/pennai
''',
    zip_safe=True,
    install_requires=['numpy>=1.16.3',
                    'scipy>=1.3.1',
                    'scikit-learn>=0.22.0',
                    'update_checker>=0.16',
                    'pandas>=0.24.2',
                    'joblib>=0.13.2',
                    'simplejson>=3.17.0'
                    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    keywords=['data science', 'machine learning','metalearning'],
)
