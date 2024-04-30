from django.contrib.auth.backends import BaseBackend

from .models import UserProfile

from string import ascii_lowercase, digits
from random import choice

from rest_framework import authentication
from rest_framework import exceptions


class AuthBackend(BaseBackend):
    supports_inactive_user = False
    supports_anonymous = False

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

    def authenticate(self, request, phone_number=None):
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            user = UserProfile(phone_number=phone_number, invite_code=self.create_unique_invite_code())
            user.save()
        return user

    @staticmethod
    def create_unique_invite_code():
        invite_codes = UserProfile.objects.values_list('invite_code', flat=True)
        simbols = ascii_lowercase + digits
        while True:
            invite_code = ''.join(choice(simbols) for _ in range(6))
            if invite_code not in invite_codes:
                return invite_code




class RestAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        phone_number = request.META.get('phone_number')
        if not phone_number:
            return None

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)