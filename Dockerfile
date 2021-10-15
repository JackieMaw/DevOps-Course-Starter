FROM python:3.8.5-slim-buster as base
RUN apt-get update
RUN pip install "poetry==1.0.0"
WORKDIR /do-me
COPY poetry.lock poetry.toml pyproject.toml /do-me/
RUN poetry install
COPY ./todo_app/ /do-me/todo_app/
EXPOSE 5000

FROM base as production
COPY ./run_gunicorn.sh ./run_gunicorn.sh
ENTRYPOINT ["./run_gunicorn.sh"]

FROM base as development
COPY ./run_flask.sh ./run_flask.sh
ENTRYPOINT ["./run_flask.sh"]
