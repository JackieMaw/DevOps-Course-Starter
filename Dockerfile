FROM python:3.8.5-slim-buster

# System deps:
RUN pip install "poetry==1.0.0"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

# Execute the Application
# ENTRYPOINT ["poetry" "run" "flask" "run"]

ENTRYPOINT ["echo", "Hello World"]