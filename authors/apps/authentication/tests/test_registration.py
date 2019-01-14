# System libraries
import json

# Third Party Libraries
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

class UserRegistrationTest(APITestCase):
    """
        Holds all user registration
    """
    def setUp(self):
        """The setup method"""
        self.register_url = reverse("auth:register")
        self.client = APIClient()

        # Define the json data
        # Data with valid user credentials
        self.valid_user_credentials = {
            "user": {
                "username":"Wachira",
                "email":"ewachira254@gmail.com",
                "password":"@Wachira254"
            }
        }
        # Data lacking a field <username>
        self.missing_field_credentials = {
            "user":{
                "username":"",
                "email":"ewachira254@gmail.com",
                "password":"@Wachira254"
            }
        }
        # Data with invalid data <password>
        self.invalid_field_credentials = {
            "user":{
                "username":"Wachira",
                "email":"ewachira254@gmail.com",
                "password":"123456"
            }
        }

    def test_user_registration(self):
        """Test the user registration"""
        response = self.client.post(
            self.register_url,
            self.valid_user_credentials,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_lacking_field(self):
        """Test lacking a field"""
        response = self.client.post(
            self.register_url,
            self.missing_field_credentials,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_field_credentials(self):
        """
            Test with invalid credentials
        """
        response = self.client.post(
            self.register_url,
            self.invalid_field_credentials,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST);
