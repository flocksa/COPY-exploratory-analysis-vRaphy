#!/bin/bash

# this script will run the app
source .venv/bin/activate
python nhanes_api.py &
cd ./frontend
npm start