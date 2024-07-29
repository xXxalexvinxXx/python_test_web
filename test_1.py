import requests
import yaml
import unittest

# Чтение конфигурации из файла config.yaml
with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class REST_Api_Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.address = data['address']
        cls.user = data['user']
        cls.password = data['pass']
        cls.title = data['title']
        cls.description = data['descript']
        cls.content = data['cont']

    def setUp(self):
        self.login_token = self.get_login_token()

    def get_login_token(self):
        res = requests.post(self.address + 'gateway/login',
                            data={'username': self.user, 'password': self.password})
        return res.json()['token']

    def create_post(self):
        header = {'X-Auth-Token': self.login_token}
        post_data = {'title': self.title, 'description': self.description, 'content': self.content}
        create_res = requests.post(self.address + 'api/posts', json=post_data, headers=header)
        self.assertEqual(create_res.status_code, 200, 'Пост не создан')
        return post_data

    def delete_post(self, post_id):
        header = {'X-Auth-Token': self.login_token}
        delete_res = requests.delete(f"{self.address}api/posts/{post_id}", headers=header)
        self.assertEqual(delete_res.status_code, 200, 'Пост не был удален')

    def test_step1(self):
        testtext1 = '123'
        header = {'X-Auth-Token': self.login_token}
        res = requests.get(self.address + 'api/posts', params={'owner': 'notMe'}, headers=header)
        listres = [i['title'] for i in res.json()['data']]
        self.assertIn(testtext1, listres)

    def test_step2(self):
        created_post = self.create_post()
        self.assertIsNotNone(created_post, 'Пост не создан')

    def test_step3(self):
        created_post = self.create_post()
        header = {'X-Auth-Token': self.login_token}
        res = requests.get(self.address + 'api/posts', headers=header)
        listres = [i['description'] for i in res.json()['data']]
        self.assertIn(created_post['description'], listres, 'Описание поста не найдено')


if __name__ == '__main__':
    unittest.main()
