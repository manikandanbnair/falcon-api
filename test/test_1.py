import json, falcon, pytest
from bson import json_util
from falcon import testing
from unittest.mock import MagicMock, patch, Mock

from service.UserService import UserModel, User, ValidationException
from app import  app

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    return mock_db

@patch('service.UserService.UserModel.exists_by_email')
def test_user_create_success(mock_exist_by_email, mock_db):
    user_model = UserModel(mock_db)
    user = User(name='John Doe', age=30, email='john@example.com')
    mock_exist_by_email.return_value = None
    user_model.user_validation(name=user.name, age=user.age, email=user.email)
    user_model.create(user)
    mock_db['user'].insert_one.assert_called_once_with({'name': 'John Doe', 'age': 30, 'email': 'john@example.com'})

@patch('service.UserService.UserModel.exists_by_email')
def test_user_create_failure_invalid_age(mock_exist_by_email, mock_db):
    user_model = UserModel(mock_db)
    user = User(name='John Doe', age=-1, email='john@example.com')
    mock_exist_by_email.return_value = None
    try:
        user_model.user_validation(name=user.name, age=user.age, email=user.email)
    except ValidationException as e:
        assert str(e) == "Invalid age"


@patch('service.UserService.UserModel.exists_by_email')
def test_user_create_failure_user_exists(mock_exists_by_email, mock_db):
    user_model = UserModel(mock_db)
    user = User(name='John Doe', age=30, email='john@example.com')
    mock_exists_by_email.return_value = {'email': 'john@example.com'}
    with pytest.raises(ValidationException):
        user_model.user_validation(name=user.name, age=user.age, email=user.email)


@patch('service.UserService.UserModel.find_all')
def test_user_resource_get_all_users(mock_find_all):
    mock_find_all.return_value = json.dumps([
        {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
        {'name': 'Jane Doe', 'age': 25, 'email': 'jane@example.com'}
    ])
    client = testing.TestClient(app)
    response = client.simulate_get('/users')
    assert response.status == falcon.HTTP_200
    assert 'Users' in response.json
    assert response.json['Users'] == [
        {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
        {'name': 'Jane Doe', 'age': 25, 'email': 'jane@example.com'}
    ]

@patch('service.UserService.UserModel.find_all')
def test_user_resource_get_all_users_no_user_present(mock_find_all):
    mock_find_all.return_value = json.dumps([])
    client = testing.TestClient(app)
    response = client.simulate_get('/users')
    assert response.status == falcon.HTTP_200
    assert response.json['Users'] == "No users present"

@patch('service.UserService.UserModel.find_by_email')
def test_user_resource_get_user_with_email(mock_find_by_email):
    mock_find_by_email.return_value = json.dumps([ {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}])
    client = testing.TestClient(app)
    response = client.simulate_get('/users', params={'email': 'john@example.com'})
    assert response.status == falcon.HTTP_200
    assert response.json['User'] == [ {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}]

@patch('service.UserService.UserModel.find_by_email')
def test_user_resource_get_user_with_email_not_found(mock_find_by_email):
    mock_find_by_email.return_value = json.dumps(None)
    client = testing.TestClient(app)
    response = client.simulate_get('/users' , params={'email': 'john@example.com'})
    assert response.status == falcon.HTTP_200
    assert response.json == {'User':'User not found'}


@patch('service.UserService.UserModel.create')
@patch('rest.UserRest.open')
def test_user_resource_create_success(mock_open, mock_create):
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([])

    client = testing.TestClient(app)
    response = client.simulate_post('/users', json={
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    })

    assert response.status == falcon.HTTP_201
    assert response.json == {"message": "Successfully created"}
    mock_create.assert_called_once_with(User(name="John Doe", age=30, email="john@example.com"))


@patch('service.UserService.UserModel.create')
@patch('rest.UserRest.open')
def test_user_resource_create_missing_fields(mock_open, mock_create, mock_db):
    mock_db['users'].find_one.return_value = None
    client = testing.TestClient(app)
    response = client.simulate_post('/users', json={
        "name": "John Doe",
        "age": 30
    })

    assert response.status == falcon.HTTP_400
    assert response.json == {"message": "Missing required fields. Please check your data and try again."}
    mock_create.assert_not_called()



@pytest.fixture
def mock_user_model(mock_db):
    user_model = UserModel(mock_db)
    user_model.collection = MagicMock()
    return user_model

def test_find_by_email(mock_user_model):
    sample_user = {
        'name': 'John Doe',
        'age': 30,
        'email': 'john@example.com'
    }
    mock_user_model.collection.find_one.return_value = sample_user
    result = mock_user_model.find_by_email('john@example.com')
    assert result == json_util.dumps(sample_user)
    mock_user_model.collection.find_one.assert_called_once_with({'email': 'john@example.com'}, {'_id': 0})

def test_find_by_email_no_user(mock_user_model):
    mock_user_model.collection.find_one.return_value = None
    result = mock_user_model.find_by_email('notfound@example.com')
    assert result == 'null'
    mock_user_model.collection.find_one.assert_called_once_with({'email': 'notfound@example.com'}, {'_id': 0})



def test_find_all_users(mock_user_model):
    sample_users = [
        {'name': 'John Doe', 'age': 30, 'email': 'john@example.com'},
        {'name': 'Jane Doe', 'age': 25, 'email': 'jane@example.com'}
    ]
    json_users = json_util.dumps(sample_users)

    mock_user_model.collection.find.return_value = [{'name': 'John Doe', 'age': 30, 'email': 'john@example.com'}, {'name': 'Jane Doe', 'age': 25, 'email': 'jane@example.com'}]

    result = mock_user_model.find_all()

    assert result == json_users


def test_validation_exception_handler():
    ex = ValidationException('Error message')
    req = Mock()
    resp = Mock()
    params = Mock()
    ValidationException.validation_exception_handler(ex, req, resp, params)
    assert resp.status == falcon.HTTP_400
    assert resp.media == {'message': ex.message}

def test_create_user_exception():
    mock_collection = Mock()
    mock_collection.insert_one.side_effect = Exception("Mocked exception")
    user = User("John Doe", 30,"john@example.com")
    with pytest.raises(Exception) as e:
        try:
            user_data = user.__dict__
            mock_collection.insert_one(user_data)
        except Exception as ex:
            raise Exception("Error creating user")
    assert str(e.value) == "Error creating user"
    mock_collection.insert_one.assert_called_once_with(user.__dict__)