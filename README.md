# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

## Enivronment Variables

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change).

## Storing Data on Trello

The application stores the tasks on Trello.
In order to set this up, please do the following:
1. Create a trello account here: https://trello.com/signup
2. Create a workspace (this will be your TRELLO_BOARD_NAME)
3. View your API Key and generate a Token: https://trello.com/app-key
5. Set the following values in the .env file:
        TRELLO_KEY=trello-key
        TRELLO_TOKEN=trello_token
        TRELLO_BOARD_NAME=ToDoApp


## Running the App with Flask

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App with Gunicorn

Once the all dependencies have been installed, launch from gunicorn within the poetry environment by running:
```bash
$ poetry run gunicorn --bind 0.0.0.0:5000 todo_app.app:create_app
```

## Setting up the Tests

You need to install Mozilla Firefox and download geckodriver.exe.
You need to copy geckodriver.exe into the root of your project and add the geckodriver.exe to your system path.

## Running the Tests

To run the unit tests and integration tests, run:

```bash
$ poetry run pytest --log-cli-level=INFO
```

Troubleshooting note - if you get this error:
        ERROR todo_app/tests_e2e/test_integration_e2e_selenium.py::test_task_journey - selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATcf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb3H.
Copy geckodriver.exe into the root of your project


## Launch within a Virtual Machine

The application can also be launched from the Vagrantfile which will setup port-forwarding from the VM port 5000 to the host machine port 5000

Trouble-shooting note:
Before the VM is provisioned, the .env file must be generated with the appropriate Trello token

## Launch within a Container

The application can also be launched from docker using the Dockerfile:

```bash
$ docker build --target development --tag do-me:dev .
$ docker run --env-file ./.env -d --publish 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/do-me/todo_app do-me:dev

$ docker build --target production --tag do-me:prod .
$ docker run --env-file ./.env -d --publish 5000:5000 do-me:prod

$ docker build --target test --tag do-me:test .
$ docker run --env-file ./.env -it do-me:test todo_app/tests

$ docker build --target exp --tag do-me:experiment .
$ docker run -it do-me:experiment

```

To launch in interactive mode add the -it flag:
```bash
$ docker run --env-file ./.env -it --publish 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/do-me/todo_app do-me:dev
$ docker run --env-file ./.env -it --publish 5000:5000 do-me:prod
```
 
## Deployed to Heroku

The application can be manually deployed to Heroku:

https://jackiemaw-do-me.herokuapp.com/

Instructions:

```bash
$ heroku login
$ heroku container:login
$ docker login
$ docker pull jackiemaw/do-me:latest
$ docker tag jackiemaw/do-me:latest registry.heroku.com/jackiemaw-do-me/web
$ docker push registry.heroku.com/jackiemaw-do-me/web
$ heroku container:release -a jackiemaw-do-me web
```

