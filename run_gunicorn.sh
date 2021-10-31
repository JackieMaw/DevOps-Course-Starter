#!/bin/bash

echo "Launching application from Gunicorn..."
poetry run gunicorn --bind 0.0.0.0:5000 todo_app.app:create_app\(\)
echo "Application launched. (hopefully)"