"""
tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the public features of the user API"""
    # public tests -> unauthenticated requests
    # i.e. registering a new user

    def setUp(self):
        self.client = APIClient()
        # creates an API Client to be used during the test

    def test_create_user_success(self):
        """test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # the content needed to create a new user
        res = self.client.post(CREATE_USER_URL, payload)
        # do a POST request to the USER_URL passing it the payload

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # check if the ENDPOINT returns a HTTP 201 creating response
        # that is the success response code for creating objs in db
        user = get_user_model().objects.get(email=payload['email'])
        # retrieves the email address from the db
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        # checks if there is any password saved for this user in the db

    def test_user_with_email_exists_error(self):
        """test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """test an error is returned if password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)