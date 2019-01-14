from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

class UserLoginTest(APITestCase):
    """
        Holds test for handling login
    """
    def setUp(self):
        """Setup method"""
        self.client = APIClient()
        self.registration_uri = reverse('auth:register')
        self.login_uri = reverse('auth:login')

        # Json data
        self.valid_login_data = {
            "user":{
                "email":"ewachira254@gmail.com",
                "password":"@Wachira254"
            }
        }
        self.valid_user_credentials = {
            "user": {
                "username":"Wachira",
                "email":"ewachira254@gmail.com",
                "password":"@Wachira254"
            }
        }

    def test_user_login(self):
        """Test login a user"""
        self.client.post(
            self.registration_uri,
            self.valid_user_credentials,
            format="json"
        )
        response = self.client.post(
            self.login_uri,
            self.valid_login_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)