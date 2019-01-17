import os
import django
import json
import re

import jwt
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.template import context
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import status
from datetime import datetime, timedelta
from .models import User
from .renderers import UserJSONRenderer
from .models import User
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetPasswordSerializer
)

from .backends import GetAuthentication
from .messages import error_msg, success_msg


class RegistrationAPIView(GenericAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
            POST /users/
        """
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        payload = {'email': serializer.data.get("email")}
        token = jwt.encode(payload, os.getenv("SECRET_KEY"),
                           algorithm='HS256').decode()
        from_mail, to_mail = os.getenv(
            "DEFAULT_FROM_EMAIL"), serializer.data.get("email")
        site_url = "http://"+get_current_site(request).domain
        subject = "Account Verification"
        link_url = site_url+"/api/users/verify/{}".format(token)
        html_page = render_to_string("email_verification.html", context={
                                     "link": link_url, "user_name": serializer.data.get("username")})
        send_mail(subject, "Verification mail", from_mail, [
                  to_mail], fail_silently=False, html_message=html_page)
        return Response({
            "username": serializer.data['username'],
            "email": serializer.data['email']
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    # Notice here that we do not call `serializer.save()` like we did for
    # the registration endpoint. This is because we don't actually have
    # anything to save. Instead, the `validate` method on our serializer
    # handles everything we need.

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyAPIView(CreateAPIView):
    """Verify endpoint holder"""
    serializer_class = UserSerializer

    def get(self, request, token):
        """
            GET /verify/
        """
        serializer = self.serializer_class()
        email = jwt.decode(token, os.getenv("SECRET_KEY"))["email"]
        user = User.objects.get(email=email)
        if user:
            user.is_confirmed = True
            user.save()

            return Response({
                "message": "Email Successfully Confirmed"
            }, status=status.HTTP_200_OK
            )
        else:
            return Response({
                "message": "No user of that email"
            }, status=status.HTTP_404_NOT_FOUND)


class PasswordResetRequestAPIView(GenericAPIView):
    """Sends Password reset link to email """
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user_data = request.data
        email = user_data['user']['email']

        # confirms if an eamil has been provided
        # if email is not given then an error message is thrown
        if not email.strip():
            return Response({
                'message': error_msg['no_email'],
            },
                status=status.HTTP_400_BAD_REQUEST)
        elif re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email) is None:
            return Response({
                'message': error_msg['email_format']
            }, status=status.HTTP_400_BAD_REQUEST)

        # confrims if a user with the given email actually exists
        # If user exists then the user instance is returned
        # the user instance is used to generate a token
        # a response is given with the email and the generated token
        elif User.objects.filter(email=email).exists():
            # fetch username using the email
            username = User.objects.all().filter(email=email).first()

            payload = {
                'email': email,
                "iat": datetime.now(),
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            token = jwt.encode(payload, os.getenv("SECRET_KEY"),
                               algorithm='HS256').decode()

            # format the email
            host = request.get_host()
            protocol = request.scheme
            reset_link = protocol + '://' + host + '/api/v1/users/password_reset/' + token
            subject = "Password Reset for Authors Haven Web Portal account"
            message = render_to_string(
                'request_password_reset.html', {
                    'email': email,
                    'token': token,
                    'username': str(username).capitalize(),
                    'link': reset_link
                })
            to_email = email
            from_email = os.getenv("DEFAULT_FROM_EMAIL")

            send_mail(
                subject,
                message,
                from_email, [
                    to_email,
                ],
                html_message=message,
                fail_silently=False)

            message = {
                'Message':
                success_msg['request_success'],
                'Token': token
            }
            return Response(message, status=status.HTTP_200_OK)

        # If user does not exist then an error is thrown to the user
        return Response({
            'message': error_msg['unregistered_email'],
        },
            status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(UpdateAPIView):
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def patch(self, request, token, **kwargs):

        # decode the token
        decoded = GetAuthentication.decode_jwt_token(token)

        # use the email to find decode the user instance
        user = User.objects.get(email=decoded['email'])

        # get the password that the user is keying in
        password = request.data['user']['password']



        # now we validate the password
        if len(password) < 8:
            return Response({
                "message": error_msg["short_pwd"]
            }, status=status.HTTP_400_BAD_REQUEST)
        elif re.search('[0-9]', password) is None:
            return Response({
                "message": error_msg["number_in_pwd"]
            }, status=status.HTTP_400_BAD_REQUEST)
        elif re.search('[a-z]', password) is None:
            return Response({
                "message": error_msg["letter_in_pwd"]
            }, status=status.HTTP_400_BAD_REQUEST)
        elif re.search('[A-Z]', password) is None:
            return Response({
                "message": error_msg["caps_in_pwd"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # save the password after we have validated it
            self.serializer_class.update(
                None,
                user,
                {
                    "password": password
                }
            )
            # Alert the user that the user has completed the password request
            return Response(
                {"message": success_msg["pwd_changed"]},
                status=status.HTTP_200_OK)
