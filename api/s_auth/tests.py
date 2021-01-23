from django.test import TestCase
from rest_framework.test import APITestCase

class AuthenticateAPITestCase(APITestCase):
    def test_SignupLogin(self):
        """signup/login api test
        """

        url = '/signup/'
        payload = {
            'email': 'test@soccer.com',
            'password': '123123',
        }
        res = self.client.post(url, data=payload)
        self.assertEqual(201, res.status_code, f'Signup api returns unexpected code: {res.status_code}')

        # test signup with the same email
        res = self.client.post(url, data=payload)
        self.assertEqual(409, res.status_code, f'Signup api (with existing email) returns unexpected code: {res.status_code}')

        # test login
        url = '/login/'
        res = self.client.post(url, data=payload)
        self.assertEqual(200, res.status_code, f'Login api returns unexpected code: {res.status_code}')
        res = res.json()
        self.assertTrue('token' in res, 'Token is not returned after login')

        # test login with invalid credentials
        res = self.client.post(url, data={
            'email': payload['email'],
            'password': payload['password'] + '-wrong',
        })
        self.assertEqual(400, res.status_code, f'Login api (with wrong credentials) returns unexpected code: {res.status_code}')

