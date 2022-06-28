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

# Data

## Storing Data on MongoDb

The application stores the tasks on MongoDb:
        cluster0.5vzof.mongodb.net
        doMeDatabase.tasks

Connection String:
        mongodb+srv://<username>:<password>@cluster0.5vzof.mongodb.net/doMeDatabase?retryWrites=true&w=majority

Set the following values in the .env file:
        MONGODB_CONNECTIONSTRING=<connectionstring>
        MONGODB_DATABASE=doMeDatabase

## Storing Data on CosmoDb (using MongoDB API)

The application stores the tasks on CosmoDb:

Connection String:
        mongodb://jackieucosmosdbaccount:<password>@jackieucosmosdbaccount.mongo.cosmos.azure.com:10255/?ssl=true

Set the following values in the .env file:
        MONGODB_CONNECTIONSTRING=<connectionstring>
        MONGODB_DATABASE=doMeDatabase

### Trouble-shooting:

pymongo.errors.OperationFailure: Retryable writes are not supported. Please disable retryable writes by specifying "retrywrites=false" in the connection string or an equivalent driver specific config., full error: {'ok': 0.0, 'errmsg': 'Retryable writes are not supported. Please disable retryable writes by specifying "retrywrites=false" in the connection string or an equivalent driver specific config.', 'code': 2, 'codeName': 'BadValue'}

# Running the App

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

# Automated Tests

## Setting up the Tests

You need to install Mozilla Firefox and download geckodriver.exe.
You need to copy geckodriver.exe into the root of your project and add the geckodriver.exe to your system path.

## Running the Tests

To run the unit tests and integration tests, run:

```bash
$ poetry run pytest --log-cli-level=INFO
```

To run only the unit tests, run:

```bash
$ poetry run pytest .\todo_app\tests --log-cli-level=INFO
```

To run only the integration tests, run:

```bash
$ poetry run pytest .\todo_app\tests_e2e --log-cli-level=INFO
```

Troubleshooting note - if you get this error:
        ERROR todo_app/tests_e2e/test_integration_e2e_selenium.py::test_task_journey - selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATcf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb3H.
Copy geckodriver.exe into the root of your project

# Deployment

## Launch within a Virtual Machine

The application can also be launched from the Vagrantfile which will setup port-forwarding from the VM port 5000 to the host machine port 5000

Trouble-shooting note:
Before the VM is provisioned, the .env file must be generated with the appropriate MONGODB tokens

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
 
## Deploying to Heroku

The application will be automatically deployed to Heroku by GitHub Actions:

https://jackiemaw-do-me.herokuapp.com/

Instructions for manual deploy:

```bash
$ heroku login
$ heroku container:login
$ docker login
$ docker pull jackiemaw/do-me:latest
$ docker tag jackiemaw/do-me:latest registry.heroku.com/jackiemaw-do-me/web
$ docker push registry.heroku.com/jackiemaw-do-me/web
$ heroku container:release -a jackiemaw-do-me web
```

All secrets must be setup on Heroku as "Config Vars":
https://dashboard.heroku.com/apps/jackiemaw-do-me/settings

## Deploying to Azure

The application will be automatically deployed to Azure by GitHub Actions:
        http://jackiemaw-do-me.azurewebsites.net/

Instructions for setting up the Azure WebApp (one-time):

```powershell
az appservice plan create --resource-group CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemawappserviceplan --sku B1 --is-linux

az webapp create --resource-group CreditSuisse21_JacquelineUngerer_ProjectExercise --plan jackiemawappserviceplan --name jackiemaw-do-me --deployment-container-image-name jackiemaw/do-me:latest

az webapp config appsettings set -g CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemaw-do-me --settings FLASK_APP=todo_app/app. 
az webapp config appsettings set -g CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemaw-do-me --settings SECRET_KEY=??? 
az webapp config appsettings set -g CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemaw-do-me --settings MONGODB_CONNECTIONSTRING=???
az webapp config appsettings set -g CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemaw-do-me --settings MONGODB_DATABASE=doMeDatabase 
az webapp config appsettings set -g CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemaw-do-me --settings CLIENT_ID=???
az webapp config appsettings set -g CreditSuisse21_JacquelineUngerer_ProjectExercise -n jackiemaw-do-me --settings CLIENT_SECRET=???
```

Instructions for manual deploy to Azure from DockerHub registry:

```bash
curl -dH -X POST <webhook>
```

To get the webhook:

```powershell
az webapp deployment container config -n jackiemaw-do-me -g CreditSuisse21_JacquelineUngerer_ProjectExercise -e true
```
### Trouble-shooting

View application logs here:
        https://jackiemaw-do-me.scm.azurewebsites.net/api/logstream

## Deploying with Kubernetes

You can deploy the application manually to Kubernetes:

```powershell
minikube start

kubectl create secret generic secrets --from-literal=db_connectionstring='<mongodb connection string>'   --from-literal=client_secret='<github client secret>' --from-literal=flask_secret='<flask session secret>'

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl port-forward service/module-14 7080:80 4
```

For troubleshooting, you can look at the status of your pods and view the logs and events:

```powershell
kubectl get pods
kubectl logs module-14-7cb9b4d97d-ct5gf
kubectl get events --sort-by=.metadata.creationTimestamp
```

To cleanup your pods and shut down:

```powershell
kubectl delete --all services
kubectl delete --all deployments
kubectl delete --all pod
minikube stop
```

# Authentication & Authorization

## OAuth with GitHub

When you first access the application, it will request User Authentication from GitHub. 
By default, all users will have UserRole "reader" which means they will not be able to create, edit or delete Tasks.
To get access to UserRole "writer" you'll have to edit the code because only JackieMaw has "writer" access :-)

Any deployed application must be registered with GitHub as an OAuth App: https://github.com/settings/developers

The following applications are already registered with GitHub:

LOCAL DEVELOPMENT
https://github.com/settings/apps/domejackie
        http://localhost:5000/
        http://localhost:5000/login/callback

PRODUCTION HEROKU
https://github.com/settings/applications/1847131
        https://jackiemaw-do-me.herokuapp.com/
        https://jackiemaw-do-me.herokuapp.com/login/callback

PRODUCTION AZURE
https://github.com/settings/applications/1857732
        https://jackiemaw-do-me.azurewebsites.net/
        https://jackiemaw-do-me.azurewebsites.net/login/callback

PRODUCTION AZURE - Deployed by Terraform
https://github.com/settings/applications/1894886	
	http://jackiemaw-do-me-now.azurewebsites.net/
	http://jackiemaw-do-me-now.azurewebsites.net/login/callback

# Logging

View recent application logs here from Azure here:
        https://jackiemaw-do-me.scm.azurewebsites.net/api/logstream

## Loggly

If you have a Loggly account, you can set LOGGLY_TOKEN as an environment variable and then the logs will be sent to Loggly.
	
# Production Deployment on Azure

## Trouble-shooting

View application logs here:
        https://jackiemaw-do-me-now.scm.azurewebsites.net/api/logstream

## Environment Variables

In order to deploy automatically to Azure via Terraform, you need to add the following Secrets for the GitHub workflow:

  ARM_CLIENT_ID
  ARM_TENANT_ID
  ARM_SUBSCRIPTION_ID
  ARM_CLIENT_SECRET
  
These can be obtained when you setup the Security Principal, for example:

az ad sp create-for-rbac --name "DoMeServicePrincipal" --role Contributor --scopes /subscriptions/d33b95c7-af3c-4247-9661-aa96d47fccc0/resourceGroups/CreditSuisse21_JacquelineUngerer_ProjectExercise

The underlying Active Directory Graph API will be replaced by Microsoft Graph API in a future version of Azure CLI. Please carefully review all breaking changes introduced during this migration: https://docs.microsoft.com/cli/azure/microsoft-graph-migration

Creating 'Contributor' role assignment under scope '/subscriptions/d33b95c7-af3c-4247-9661-aa96d47fccc0/resourceGroups/CreditSuisse21_JacquelineUngerer_ProjectExercise'
The output includes credentials that you must protect. Be sure that you do not include these credentials in your code or check the credentials into your source control. For more information, see https://aka.ms/azadsp-cli
{
  "appId": "2b0ca477-e125-40b9-b9d8-c03ff4913bae",
  "displayName": "DoMeServicePrincipal",
  "password": *****,
  "tenant": "7d6f97d6-d755-4c10-b763-409cc4b6638f"
}
