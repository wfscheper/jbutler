# Copyright (c) 2013 SAS Institute, Inc
#
from setuptools import find_packages, setup


requires = [
    'setuptools',
    'jenkinsapi',
    ]


VERSION = (0, 0, 1)

setup(
    name='jbutler',
    version='{0}.{1}.{2}'.format(*VERSION),
    description='Manage a Jenkins instance',
    author='Walter Scheper',
    author_email='walter.scheper@sas.com',
    license='Apache License 2.0',
    install_requires=requires,
    packages=find_packages(),
    scripts=['commands/jbutler']
    )
