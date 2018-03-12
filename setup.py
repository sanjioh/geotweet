from setuptools import find_packages, setup

NAME = 'geotweet'
DESCRIPTION = 'Fetch geolocalized tweets and plot them on a map.'
URL = 'https://github.com/sanjioh/geotweet'
AUTHOR = 'Fabio Sangiovanni'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['geotweet=geotweet.geotweet:main'],
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
