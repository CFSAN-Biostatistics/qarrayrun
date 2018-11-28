#!/bin/bash

rm -r qarrayrun.egg-info/
python setup.py clean --all
python setup.py sdist --verbose

