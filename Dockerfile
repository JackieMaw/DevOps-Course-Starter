FROM python:3.8.5-slim-buster
RUN apt-get update
RUN pip install "poetry==1.0.0"
WORKDIR /opt/do-me/bin
COPY . /do-me
RUN chmod +x do-me
COPY ./run.sh ./run.sh
RUN chmod +x ./run.sh
EXPOSE 5000
ENTRYPOINT ["./run.sh"]