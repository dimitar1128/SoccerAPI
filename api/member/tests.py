from django.test import TestCase
from rest_framework.test import APITestCase
import pandas as pd
from database.soccer.models import *

class MemberTestCase(APITestCase):
    def test_MemberCRUD(self):
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

        url = '/member/'
        # create member
        res = self.client.post(url, data={
            'token': token,
        })
        assert res.status_code == 201, f'Member create api returns unexpected code: {res.status_code}'

        # get member
        res = self.client.get(url, data={
            'token': token
        })
        assert res.status_code == 200, f'Member get api returns unexpected code: {res.status_code}'
        res = res.json()
        df = pd.DataFrame(res)
        expected_columns = [
            'id', 'first_name', 'last_name', 'country', 'age', 'type', 'value', 'team_id',
        ]
        assert set(expected_columns) == set(df.columns), 'Member get api returns unexpected columns'

        # update team
        res = self.client.put(url, data={
            'token': token,
            'id': 1,
            'first_name': 'New first name',
        })
        assert res.status_code == 200, f'Member update api returns unexpected code: {res.status_code}'

        # delete member
        res = self.client.delete(url, data={
            'token': token,
            'id': 1,
        })
        assert res.status_code == 204, f'Member delete api returns unexpected code: {res.status_code}'

        res = self.client.get(url, data={
            'token': token
        })
        assert res.status_code == 200, f'Member get api returns unexpected code: {res.status_code}'
        res = res.json()
        assert len(res) == 0, 'Member is not deleted'


    def testNewMemberToTeam(self):
        """test register new member to an existing team"""
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
        admin_token = res.json()['token']

        # signup a new user to create his team
        url = '/signup/'
        res = self.client.post(url, data={
            'email': 'user1@soccer.com',
            'password': '123123',
        })
        assert res.status_code == 201, f'Signup api returns unexpected code: {res.status_code}'

        url = '/login/'
        res = self.client.post(url, data={
            'email': 'user1@soccer.com',
            'password': 123123,
        })
        assert res.status_code == 200, f'Login api returns unexpected code: {res.status_code}'
        user_token = res.json()['token']

        # register a new member and to the team
        url = '/member/'
        res = self.client.post(url, data={
            'token': admin_token,
            'first_name': 'New member',
            'team_id': 1,
        })
        assert res.status_code == 201, f'New member to team api returns unexpected code: {res.status_code}'
        res = res.json()
        member_id = res['member_id']

        # get user's team
        url = '/my_team/'
        res = self.client.get(url, data={
            'token': user_token,
        })
        assert res.status_code == 200, f'Get my_team api returns unexpected code: {res.status_code}'
        res = res.json()

        member_ids = [member['id'] for member in res['members']]
        assert member_id in member_ids, f'New member is not registered to the user\'s team'



    def testNewMemberToMarket(self):
        """test register new member to market"""
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

        # register a new member and to the market
        url = '/member/'
        res = self.client.post(url, data={
            'token': token,
            'first_name': 'New member',
            'market_price': 100000,
        })
        assert res.status_code == 201, f'New member to market api returns unexpected code: {res.status_code}'
        res = res.json()
        member_id = res['member_id']

        # read market members
        url = '/market/'
        res = self.client.get(url, data={
            'token': token,
        })
        res = res.json()

        member_ids = [member['id'] for member in res]
        assert member_id in member_ids, 'Member is not set on the market'