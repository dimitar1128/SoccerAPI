from django.test import TestCase
from rest_framework.test import APITestCase
import pandas as pd

class MarketApiTestCase(APITestCase):
    def testSetPlayerOnMarketAndList(self):
        """test set player on market, and list all market players api"""
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

        url = '/market/'
        payload = {
            'token': token,
            'member_id': 1,
            'price': 30000,
        }
        res = self.client.post(url, data=payload)
        assert res.status_code == 201, f'SetPlayerOnMarket api returns unexpected code: {res.status_code}'

        # test with invalid payload
        payload = {
            'token': token,
            'member_id': 1,
        }
        res = self.client.post(url, data=payload)
        assert res.status_code == 400, f'SetPlayerOnMarket api (without price) returns unexpected code: {res.status_code}'

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


    def testBuyMemberOnMarket(self):
        """test buy member on market api
        """
        """test set player on market, and list all market players api"""
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

        url = '/market/'
        payload = {
            'token': token,
            'member_id': 1,
            'price': 30000,
        }
        res = self.client.post(url, data=payload)
        assert res.status_code == 201, f'SetPlayerOnMarket api returns unexpected code: {res.status_code}'

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


