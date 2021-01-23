from django.test import TestCase
from rest_framework.test import APITestCase
from database.soccer.models import *
import pandas as pd

class UserTestCase(APITestCase):
    def testUserCRUD(self):
        # create administrator account, and login
        admin = TBLUser()
        admin.email = 'admin@soccer.com'
        admin.username = 'admin@soccer.com'
        admin.is_superuser = 1
        admin.set_password('123123')
        admin.save()

        url = '/login/'
        res = self.client.post(url, data={
            'email': 'admin@soccer.com',
            'password': '123123'
        })
        assert res.status_code == 200, f'Login api returns unexpected code: {res.status_code}'
        token = res.json()['token']

        url = '/user/'
        # create user
        res = self.client.post(url, data={
            'token': token,
            'email': 'user1@soccer.com',
            'password': '123123'
        })
        assert res.status_code == 201, f'User create api returns unexpected code: {res.status_code}'

        # get users
        res = self.client.get(url, data={
            'token': token,
        })
        assert res.status_code == 200, f'User get api returns unexpected code: {res.status_code}'
        res = res.json()

        df = pd.DataFrame(res)
        expected_columns = [
            'id', 'email', 'password',
        ]
        assert set(expected_columns) == set(df.columns), 'User get api returns unexpected columns'

        # update user
        user_email = res[0]['email']
        res = self.client.put(url, data={
            'token': token,
            'email': user_email,
            'password': 'new password'
        })
        assert res.status_code == 200, f'User update api returns unexpected code: {res.status_code}'

        # delete user
        res = self.client.delete(url, data={
            'token': token,
            'email': user_email,
        })
        assert res.status_code == 204, f'User delete api returns unexpected code: {res.status_code}'

        res = self.client.get(url, data={
            'token': token,
        })
        assert res.status_code == 200, f'User get api returns unexpected code: {res.status_code}'
        res = res.json()

        assert len(res) == 0, f'User is not deleted'





