#!/bin/bash

echo "Launching application from Flask..."
poetry run flask run --host=0.0.0.0
echo "Application launched. (hopefully)"