import secrets

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()


pytestmark = pytest.mark.django_db


class TestLoginViews:

    endpoint = "/login/"

    def test_view(self, api_client):
        response = api_client.get(self.endpoint)

        assert response.status_code == 200

    def test_login(self, api_client):
        user = baker.prepare(User)
        new_password = secrets.token_hex(8)
        user.set_password(new_password)
        user.save()
        user_data = {"username": user.username, "password": new_password}
        url = f"{self.endpoint}auth/"
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == 200
        assert Token.objects.all().count() == 1
