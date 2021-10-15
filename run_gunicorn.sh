#!/bin/bash

echo "Launching gunicorn application..."
poetry run flask run --host=0.0.0.0
#poetry run gunicorn --bind 0.0.0.0:5000 wsgi:app
echo "Application launched. (hopefully)"