#!/usr/bin/bash

# run api
pip install --trusted-host pypi.python.org -r API/requirements.txt
cd API
python3 run.py
cd ..
