#!/bin/bash

echo "Launching application from Gunicorn..."
poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:$PORT
echo "Application launched. (hopefully)"