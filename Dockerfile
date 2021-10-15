FROM python:3.8.5-slim-buster as base
RUN apt-get update
RUN pip install "poetry==1.0.0"
WORKDIR /do-me
COPY poetry.lock poetry.toml pyproject.toml /do-me/
RUN poetry install
COPY ./todo_app/ /do-me/todo_app/
COPY ./run.sh ./run.sh
EXPOSE 5000
ENTRYPOINT ["./run.sh"]
