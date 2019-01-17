import jwt
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


class JWTokens(object):
    """
    Handles token generation

    """
    def create_token(self, user):
        """
        Create and return the user's JWT token

        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return token
