import json, mongomock,falcon
from falcon import testing
from unittest.mock import MagicMock, patch
import pytest

from mongo_manager.connection import DatabaseConnection
from mongo_manager.mongo_manager import MongoManager


@pytest.fixture
def mock_database_connection():
    mock_db = mongomock.MongoClient().test_db
    with patch('mongo_manager.connection.DatabaseConnection.connect_to_mongo', return_value=mock_db):
        yield mock_db




@pytest.fixture
def client(mock_database_connection):
    from app import app
    with patch('mongo_manager.mongo_manager.MongoManager') as mock_mongo_manager:
        mock_mongo_manager.return_value.collection = mock_database_connection.users
        yield testing.TestClient(app)



def test_user_create_failure_user_exists(mock_database_connection, client):

    existing_user = {
        "name": "Jon snow",
        "age": 30,
        "email": "jonsno@example.com"
    }
    mock_database_connection.users.insert_one(existing_user)

    response = client.simulate_post('/user', json={
        "name": "Jon snow",
        "age": 30,
        "email": "jonsno@example.com"
    })


    assert response.status == falcon.HTTP_400
    assert response.json['message'] == "User already exists"

    mock_database_connection.users.delete_many({})


def test_user_resource_get_all_users_no_user_present(mock_database_connection,client):
    mock_database_connection.users.delete_many({})
    response = client.simulate_get('/users')
    assert response.status == falcon.HTTP_200
    assert response.json['message'] == "No users present"


@patch('rest.UserRest.open')
def test_write_user_data_exception(mock_open_instance, client, mock_database_connection):
    mock_open_instance.side_effect = Exception("File operation failed")

    response = client.simulate_post('/user', json={
        "name": "Mary Jane",
        "age": 33,
        "email": "mary@example.com"
    })

    assert response.status == falcon.HTTP_400
    assert response.json == {'message': 'Error in writing file.'}

    mock_database_connection.users.delete_many({})

@patch('rest.UserRest.open')
def test_user_resource_create_success(mock_open_instance, client, mock_database_connection):

    mock_open_instance.return_value.__enter__.return_value.read.return_value = json.dumps([])

    response = client.simulate_post('/user', json={
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    })

    assert response.status == falcon.HTTP_201
    assert response.json == {"message": "Successfully created"}






def test_user_create_failure_invalid_age(mock_database_connection,client):
    response = client.simulate_post('/user', json={
        "name": "John Doe",
        "age": -1,
        "email": "john@example.com"
    })

    assert response.status == falcon.HTTP_400
    assert response.json['message'] == "Invalid age"




def test_user_resource_create_missing_fields(mock_database_connection,client):
    response = client.simulate_post('/user', json={
        "name": "John Doe",
        "age": 30
    })
    assert response.status == falcon.HTTP_400
    assert response.json == {"message": "Missing required fields. Please check your data and try again."}





def test_user_resource_get_user_with_email(mock_database_connection, client):
    db = mock_database_connection
    sample_user = {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}


    db.users.insert_one(sample_user)

    response = client.simulate_get('/users', params={'email': 'john@example.com'})

    assert response.status == falcon.HTTP_200
    returned_user = response.json['User']
    assert returned_user['name'] == sample_user['name']
    assert returned_user['age'] == sample_user['age']
    assert returned_user['email'] == sample_user['email']



def test_user_resource_get_all_users(mock_database_connection, client):

    db = mock_database_connection


    db.users.insert_one({'name': 'John Doe', 'age': 30, 'email': 'john@example.com'})



    sample_users = [
        {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},

    ]

    #
    response = client.simulate_get('/users')


    assert response.status == falcon.HTTP_200

    assert 'Users' in response.json


    assert response.json['Users'] == sample_users


def test_user_resource_get_user_with_email_not_found( mock_database_connection,client):
    db=mock_database_connection
    response = client.simulate_get('/users', params={'email': 'don@example.com'})
    assert response.status == falcon.HTTP_200
    assert response.json == {'message': 'User not found'}


def test_insert_user_raises_exception():

    mock_collection = MagicMock()
    mock_collection.insert_one.side_effect = Exception("Insert failed")

    mock_db_connection = MagicMock()
    mock_db_connection.__getitem__.return_value = mock_collection

    mongo_manager = MongoManager(mock_db_connection, collection_name="users")

    user_data = {
        "name": "Test User",
        "age": 25,
        "email": "testuser@example.com"
    }

    with pytest.raises(Exception) as exc_info:
        mongo_manager.insert(user_data)

    assert str(exc_info.value) == "Error creating user"


def test_connect_to_mongo_raises_exception():

    with patch('configparser.ConfigParser') as mock_config:
        mock_config_instance = mock_config.return_value
        mock_config_instance.__getitem__.side_effect = lambda key: {
            'database': {
                'MONGO_HOST': 'localhost',
                'MONGO_PORT': 27017,
                'MONGO_DB_NAME': 'test_db'
            }
        }[key]

        with patch('pymongo.MongoClient') as mock_mongo_client:

            mock_mongo_client.side_effect = ConnectionError("Failed to connect")

            with pytest.raises(Exception) as exc_info:
                DatabaseConnection.connect_to_mongo()

            assert str(exc_info.value) == "Could not connect to MongoDB: Failed to connect"