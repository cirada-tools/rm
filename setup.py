#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'RM-Tools'
DESCRIPTION = 'RM-synthesis, RM-clean and QU-fitting on polarised radio spectra'
URL = 'https://github.com/CIRADA-Tools/RM-Tools'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '1.0.7'
DOWNLOAD_URL = 'https://github.com/CIRADA-Tools/RM-Tools/archive/v'+VERSION+'.tar.gz'

REQUIRED = [
    'numpy', 'scipy', 'matplotlib', 'astropy',
]

extras_require={'QUfitting': ['pymultinest'],'parallel':["schwimmbad"]}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=REQUIRES_PYTHON,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=['RMtools_1D', 'RMtools_3D', 'RMutils'],
    entry_points={
        'console_scripts': ['rmsynth3d=RMtools_3D.do_RMsynth_3D:main',
                            'rmclean3d=RMtools_3D.do_RMclean_3D:main',
                            'rmsynth1d=RMtools_1D.do_RMsynth_1D:main',
                            'rmclean1d=RMtools_1D.do_RMclean_1D:main',
                            'rmsynth1dFITS=RMtools_1D.do_RMsynth_1D_fromFITS:main',
                            'qufit=RMtools_1D.do_QUfit_1D_mnest:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    maintainer='Cameron Van Eck',
    maintainer_email='cameron.van.eck@dunlap.utoronto.ca',
    test_suite='tests',
)
