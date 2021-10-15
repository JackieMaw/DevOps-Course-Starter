#!/bin/bash

echo "Launching flask application..."
poetry run flask run --host=0.0.0.0
echo "Application launched. (hopefully)"