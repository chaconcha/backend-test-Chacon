import pytest
from rest_framework.test import APIClient

from model_bakery import baker

from ..models import Menu


@pytest.fixture
def api_client():
    return APIClient()


pytestmark = pytest.mark.django_db


class TestMenuViews:

    endpoint = "/menu/"

    def test_list(self, api_client):
        response = api_client.get(self.endpoint)

        assert response.status_code == 200

    def test_response(self, api_client):
        menu = baker.prepare(Menu)
        url = f"{self.endpoint}{menu.id}/"
        response = api_client.get(url)

        assert response.status_code == 200

    def test_detail(self, api_client):
        menu = baker.prepare(Menu)
        url = f"{self.endpoint}{menu.id}/detail/"
        response = api_client.get(url)

        assert response.status_code == 200
