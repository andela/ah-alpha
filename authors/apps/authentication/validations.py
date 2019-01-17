import re
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

# Local imports
from .messages import error_msg
from .models import User


class UserValidation():
    """
    This is to validate user input on registration and login and return
    descriptive validation error messages
    """

    def valid_email(self, email=None):
        """
        Function to validate the user email on registration
        """
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError(error_msg['usedemail'])
        elif re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email) is None:
            raise ValidationError(error_msg['email_format'])
        return True

    def valid_username(self, username=None):
        """
        Function to validate the username on registration
        """
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError(error_msg['usedname'])
        elif len(username) < 3:
            raise ValidationError(error_msg['shortname'])
        elif re.search('[A-Za-z]', username) is None:
            raise ValidationError(error_msg['no_letter'])
        elif re.match('[A-Za-z]|[0-9]', username) is None:
            raise ValidationError(error_msg['special_character'])
        return True

    def valid_password(self, password=None):
        """
        Function to validate the user password on registration
        """
        if len(password) < 8:
            raise ValidationError(error_msg['short_pwd'])
        elif re.search('[0-9]',password) is None:
            raise ValidationError(error_msg['number_in_pwd'])
        elif re.search('[a-z]', password) is None:
            raise ValidationError(error_msg['letter_in_pwd'])
        elif re.search('[A-Z]', password) is None:
            raise ValidationError(error_msg['caps_in_pwd'])
        return True

    def valid_login_email(self, email=None):
        """
        Function to validate the user email on registration
        """
        user_qs = User.objects.filter(email=email)
        if re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email) is None:
            raise ValidationError(error_msg['email_format'])
        elif not user_qs.exists():
            raise ValidationError(error_msg['unregistered_email'])
        return True
