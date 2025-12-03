#!/bin/bash

# this script will run the app
source .venv/bin/activate
python nhanes_api.py &
cd ./frontend
npm install react-select react-plotly.js plotly.js
npm start