""" import pytest
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from requests.auth import AuthBase
from django.contrib.auth.models import User
from rest_framework.response import Response
import requests
# Create your tests here.


class BaseClass(APITestCase):
    loggeduser = {}

    user = {
        "username": "admin3",
        "password": "Admin101#",
        'email': 'admin3@gmail.com'
    }
    login = {
        "username": "admin3",
        "password": "Admin101#"
    }

    def auth_user(self):
        payload = {'name': 'Test'}
        createduser = self.client.post('/auth/users/', self.user)
        response = self.client.post('/auth/jwt/create/', self.login)
        print(response.data)
        # print('Hello test ', response.data.get('access'))
        header = {'Authorization': 'Bearer '+response.data.get("access")}
        print("hhsdskjv here")
        print(requests.post(
            'http://127.0.0.1:8000/api/transactiontypes/', payload, headers=header))

        c = APIClient()
        tt = User.objects.get(pk=createduser.data.get('id'))
        c.force_authenticate(user=tt,
                             token='Bearer '+response.data.get("access"))

        response = c.post('/api/transactiontypes/', payload)
        print("result", response)

    def test_anonymous_user_fail_return_401(self):
        pass
        # response = self.client.get('/api/transactiontypes/')
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_transaction_type_return_201_created(self):
        c = APIClient()
        res = self.auth_user()
        # c.force_authenticate(user=res[1], token=res[0])
        print('header------', c.credentials)
        # c.credentials(HTTP_AUTHORIZATION='Bearer '+self.auth_user)
        # self.auth_user()
        payload = {'name': 'Test'}
        response = c.post('/api/transactiontypes/', payload)
        print("result", response)
        # self.assertEqual(response.data.get('name'), 'TEST')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 """
