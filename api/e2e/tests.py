from django.test import TestCase
from rest_framework.test import APITestCase
import pandas as pd

class E2ETest(APITestCase):
    def test_e2e(self):
        """signup/login api test
                """

        url = '/signup/'
        payload = {
            'email': 'test@soccer.com',
            'password': '123123',
        }
        res = self.client.post(url, data=payload)
        self.assertEqual(201, res.status_code, f'Signup api returns unexpected code: {res.status_code}')

        # test login
        url = '/login/'
        res = self.client.post(url, data=payload)
        self.assertEqual(200, res.status_code, f'Login api returns unexpected code: {res.status_code}')
        res = res.json()
        self.assertTrue('token' in res, 'Token is not returned after login')

        token = res['token']

        # test get my_team api
        url = '/my_team/'
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

        # set player on the market
        url = '/market/'
        payload = {
            'token': token,
            'member_id': 1,
            'price': 30000,
        }
        res = self.client.post(url, data=payload)
        assert res.status_code == 201, f'SetPlayerOnMarket api returns unexpected code: {res.status_code}'

        # test market list, including filtering
        payload = {
            'token': token,
            'filter_value_lte': 100000,
        }
        res = self.client.get(url, data=payload)
        assert res.status_code == 200, f'MarketList api returns unexpected code: {res.status_code}'

        res = res.json()
        assert len(res) == 1, f'MarketList api returns unexpected number of members: {len(res)}'

        df = pd.DataFrame(res)
        expected_columns = [
            'id', 'first_name', 'last_name', 'country', 'team_name', 'price'
        ]
        assert set(expected_columns) == set(df.columns), 'MarketList api returns unexpected columns'

        # signup with another email
        url = '/signup/'
        payload = {
            'email': 'test1@soccer.com',
            'password': '123123',
        }
        res = self.client.post(url, data=payload)
        assert res.status_code == 201, f'Signup api returns unexpected code: {res.status_code}'

        url = '/login/'
        res = self.client.post(url, data=payload)
        assert res.status_code == 200, f'Login api returns unexpected code: {res.status_code}'
        token = res.json()['token']

        # buy player on the market
        url = '/market/'
        payload = {
            'token': token,
            'member_id': 1,
        }
        res = self.client.put(url, data=payload)
        assert res.status_code == 200, f'BuyMember api returns unexpected code: {res.status_code}'

        # check if the member is moved to the team
        url = '/my_team/'
        payload = {
            'token': token
        }
        res = self.client.get(url, data=payload)
        assert res.status_code == 200, f'GetMyTeam api returns unexpected code: {res.status_code}'

        res = res.json()
        member_ids = [member['id'] for member in res['members']]
        assert 1 in member_ids, f'Member was not moved to the team'