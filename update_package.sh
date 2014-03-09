#!/usr/bin/env sh
python setup.py sdist upload
python setup.py bdist_wheel upload
