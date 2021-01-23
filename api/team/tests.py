from django.test import TestCase
from rest_framework.test import APITestCase
import pandas as pd
from database.soccer.models import *

class MyTeamApiTestCase(APITestCase):
    def testGetAndUpdateMyteam(self):
        """get/update my_team api test
        """
        url = '/signup/'
        payload = {
            'email': 'test@soccer.com',
            'password': '123123',
        }
        res = self.client.post(url, data=payload)
        assert res.status_code == 201, f'Signup api returns unexpected code: {res.status_code}'

        url = '/login/'
        res = self.client.post(url, data=payload)
        assert res.status_code == 200, f'Login api returns unexpected code: {res.status_code}'
        token = res.json()['token']

        # test get my_team api with invalid token
        url = '/my_team/'
        res = self.client.get(url, data={'token': token + '-wrong'})
        assert res.status_code == 401, f'Get my_team api (with wrong token) returns unexpected code: {res.status_code}'

        # test get my_team api
        res = self.client.get(url, data={'token': token})
        assert res.status_code == 200, f'Get my_team api returns unexpected code: {res.status_code}'
        res = res.json()
        df = pd.DataFrame(res)

        expected_columns = [
            'id', 'owner_id', 'name', 'country', 'extra_value', 'total_value', 'members'
        ]
        assert set(expected_columns) == set(df.columns), 'Get my_team api returns unexpected columns'

        member_id = res['members'][0]['id']
        # test update my_team api
        payload = {
            'token': token,
            'team_name': 'New team name',
            'team_country': 'New team country',
            'member_id': member_id,
            'member_first_name': 'New first name',
            'member_last_name': 'New last name',
            'member_country': 'New country',
        }
        res = self.client.put(url, data=payload)
        assert res.status_code == 200, f'Update my_team api returns unexpected code: {res.status_code}'

        res = self.client.get(url, data={'token': token})
        assert res.status_code == 200, f'Get my_team api returns unexpected code: {res.status_code}'
        res = res.json()
        assert res['name'] == payload['team_name'], 'Team name is not updated'
        assert res['country'] == payload['team_country'], 'Team country name is not updated'
        assert res['members'][0]['first_name'] == payload['member_first_name'], 'Member first name is not updated'
        assert res['members'][0]['last_name'] == payload['member_last_name'], 'Member last name is not updated'
        assert res['members'][0]['country'] == payload['member_country'], 'Member country name is not updated'



class TeamTestCase(APITestCase):
    def testTeamCRUD(self):
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

        url = '/team/'
        # create team
        res = self.client.post(url, data={
            'token': token,
            'name': 'Team 1',
            'country': 'Bulgaria',
        })
        assert res.status_code == 201, f'Team create api returns unexpected code: {res.status_code}'

        # get team
        res = self.client.get(url, data={
            'token': token
        })
        assert res.status_code == 200, f'Team get api returns unexpected code: {res.status_code}'
        res = res.json()
        df = pd.DataFrame(res)
        expected_columns = [
            'id', 'owner_id', 'name', 'country', 'extra_value', 'total_value', 'members',
        ]
        assert set(expected_columns) == set(df.columns), 'Team get api returns unexpected columns'

        # update team
        res = self.client.put(url, data={
            'token': token,
            'id': 1,
            'name': 'New team name',
        })
        assert res.status_code == 200, f'Team update api returns unexpected code: {res.status_code}'

        # delete team
        res = self.client.delete(url, data={
            'token': token,
            'id': 1,
        })
        assert res.status_code == 204, f'Team delete api returns unexpected code: {res.status_code}'

        res = self.client.get(url, data={
            'token': token
        })
        assert res.status_code == 200, f'Team get api returns unexpected code: {res.status_code}'
        res = res.json()
        assert len(res) == 0, 'Team is not deleted'

