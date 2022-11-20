#!/usr/bin/bash

# run api
pip install --trusted-host pypi.python.org -r API/requirements.txt
cd API
python3 run.py
cd ..

# run frontend
npm install -g npm
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
npm install axios
cd GUI/frontend
npm start
