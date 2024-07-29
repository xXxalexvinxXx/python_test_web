import pytest
import yaml
import requests

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def login():
    res1 = requests.post(data['address'] + 'gateway/login',
                         data={'username': data['user'], 'password': data['pass']})
    print(res1.content)
    return res1.json()['token']


@pytest.fixture()
def testtext1():
    return '123'


@pytest.fixture()
def create_post(login):
    header = {'X-Auth-Token': login}
    # Данные для создания нового поста
    post_data = {'title': data['title'], 'description': data['descript'], 'content': data['cont']}
    create_res = requests.post(data['address'] + 'api/posts', json=post_data, headers=header)
    assert create_res.status_code == 200, 'Пост не создан'

    return post_data


@pytest.fixture()
def delete_post(login):
    def _delete_post(post_id):
        header = {'X-Auth-Token': login}
        delete_res = requests.delete(f"{data['address']}api/posts/{post_id}", headers=header)
        assert delete_res.status_code == 200, 'Пост не был удален'

    return _delete_post
