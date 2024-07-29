import requests
import yaml

# Чтение конфигурации из файла config.yaml
with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


def test_step1(login, testtext1):
    # Создание заголовка с токеном аутентификации
    header = {'X-Auth-Token': login}
    # Отправка GET-запроса для получения списка постов
    res = requests.get(data['address'] + 'api/posts', params={'owner': 'notMe'}, headers=header)
    listres = [i['title'] for i in res.json()['data']]
    # Проверка, что testtext1 присутствует в списке заголовков постов
    assert testtext1 in listres


def test_step2(login, create_post):
    #Проверка успешного создания поста
    assert create_post is not None, 'Пост не создан'


def test_step3(login, create_post):
    header = {'X-Auth-Token': login}

    # Отправка GET-запроса для получения списка постов
    res = requests.get(data['address'] + 'api/posts', headers=header)
    listres = [i['description'] for i in res.json()['data']]

    # Проверка, что описание созданного поста присутствует в списке описаний постов
    assert create_post['description'] in listres, 'Описание поста не найдено'
