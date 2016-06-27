#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "pigshare",
    "influxdb"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='figshare_uoa_stats',
    version='0.1.0',
    description="Script to feed figshare stats into influxdb",
    long_description=readme + '\n\n' + history,
    author="Markus Binsteiner",
    author_email='makkus@gmail.com',
    url='https://github.com/makkus/figshare_uoa_stats',
    packages=[
        'figshare_uoa_stats',
    ],
    package_dir={'figshare_uoa_stats':
                 'figshare_uoa_stats'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='figshare_uoa_stats',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'figshare_stats = figshare_uoa_stats.figshare_uoa_stats:run'
        ]
    }

)
