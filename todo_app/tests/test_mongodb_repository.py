import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from unittest.mock import Mock, patch
import json
from data import mongodb_repository

connection_string = "mongodb+srv://jmaw1:ppppp@cluster0.5vzof.mongodb.net/doMeDatabase?retryWrites=true&w=majority"
dbname = "doMeDatabase"

def test_get_tasks():
    repo = mongodb_repository(connection_string, dbname)
    tasks = repo.get_tasks()
    
    assert tasks.count() == 2