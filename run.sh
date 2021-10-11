#!/bin/bash

echo "Launching flask application..."
nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
echo "Application launched. (hopefully)"