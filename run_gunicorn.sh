#!/bin/bash

echo "Launching gunicorn application..."
poetry run flask run --host=0.0.0.0
echo "Application launched. (hopefully)"