from server import app
from fastapi.testclient import TestClient
import pytest
from chatapp.schemas import *
from faker import Faker
from fastapi.security import HTTPBasicCredentials
import random
fake = Faker('en_US')

global_user_id_pass = {}
global_jwt = ""


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as _client:
        yield _client


def test_create_user(client: TestClient):
    for i in range(5):
        name = fake.name()
        username = name.replace(" ", "").lower()
        password = fake.password()
        global_user_id_pass[username] = [password]
        data = UserCreate(username=username, password=password,
                          name=name, profession="Software Engineer")
        response = client.post(
            '/users', json=dict(data))
        print(response.json())
        global_user_id_pass[username].append(response.json()['id'])
        print(global_user_id_pass)
        assert response.status_code == 200
        assert response.json() is not None


def test_edit_user(client: TestClient):
    for username, (password, user_id) in global_user_id_pass.items():
        new_name = fake.name()
        new_profession = fake.word()
        new_user = UserUpdate(name=new_name, profession=new_profession)
        response = client.put(f'/users/{user_id}', json=dict(new_user))
        print(response.json())
        assert response.status_code == 200


def test_login(client: TestClient):
    global global_jwt
    username = list(global_user_id_pass.keys())[0]
    password = global_user_id_pass[username][0]
    data = HTTPBasicCredentials(username=username, password=password)
    response = client.post(
        '/auth/login', json=dict(data))
    print(response.json())
    global_jwt = response.json()['token']
    print(global_jwt)
    assert response.status_code == 200


def test_create_group(client: TestClient):
    global global_jwt
    member_ids = [str(i[1]) for i in global_user_id_pass.values()]
    for i in range(5):
        groupname = "GRP_" + fake.word()
        members = random.sample(member_ids, random.randint(0, len(member_ids)))
        data = GroupCreate(name=groupname, members=members)
        headers = {"Authorization": f"Bearer {global_jwt}"}
        print("In test create group", global_jwt)
        response = client.post(
            '/groups', headers=headers, json=dict(data))
        print(response.json())
        assert response.status_code == 200


def test_get_group(client: TestClient):
    global global_jwt
    criteria = "all"
    headers = {"Authorization": f"Bearer {global_jwt}"}
    response = client.get(f'/groups?criteria={criteria}', headers=headers)
    print(response.json())
    assert response.status_code == 200


def test_delete_group(client: TestClient):
    global global_jwt

    group_id = random.randint(1, 5)
    headers = {"Authorization": f"Bearer {global_jwt}"}
    response = client.delete(f'/groups/{group_id}', headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'message': 'Group deleted successfully'}
