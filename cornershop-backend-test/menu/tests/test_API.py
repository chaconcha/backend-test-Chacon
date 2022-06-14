import json

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from model_bakery import baker

from ..models import Menu, MenuResponse


@pytest.fixture
def auth_api_client():
    token = baker.make(Token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def api_client():
    return APIClient()


pytestmark = pytest.mark.django_db


class TestMenuEndpoints:

    endpoint = "/menu-api/"

    def test_list(self, auth_api_client):
        baker.make(Menu, _quantity=3)

        response = auth_api_client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, auth_api_client):
        menu = baker.prepare(Menu)
        expected_json = {
            "name": menu.name,
            "date": str(menu.date),
            "options": [],
            "responses": [],
        }
        response = auth_api_client.post(
            self.endpoint, data=expected_json, format="json"
        )
        # removes uuid for comparison, since it's dinamically generated
        response_content = json.loads(response.content)
        response_content.pop("id")

        assert response.status_code == 201
        assert response_content == expected_json

    def test_retrieve(self, auth_api_client):
        menu = baker.make(Menu)
        expected_json = {
            "id": str(menu.id),
            "name": menu.name,
            "date": str(menu.date),
            "options": [],
            "responses": [],
        }
        url = f"{self.endpoint}{menu.id}/"

        response = auth_api_client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, rf, auth_api_client):
        old_menu = baker.make(Menu)
        new_menu = baker.prepare(Menu)
        menu_dict = {
            "name": new_menu.name,
            "date": str(new_menu.date),
            "options": [],
            "responses": [],
        }

        url = f"{self.endpoint}{old_menu.id}/"

        response = auth_api_client.put(url, menu_dict, format="json")
        # removes uuid for comparison, since it's dinamically generated
        response_content = json.loads(response.content)
        response_content.pop("id")

        assert response.status_code == 200
        assert response_content == menu_dict

    def test_delete(self, mocker, auth_api_client):
        menu = baker.make(Menu)
        url = f"{self.endpoint}{menu.id}/"

        response = auth_api_client.delete(url)

        assert response.status_code == 204
        assert Menu.objects.all().count() == 0

    def test_form(self, api_client):
        menu = baker.make(Menu)
        expected_json = {
            "id": str(menu.id),
            "name": menu.name,
            "date": str(menu.date),
            "options": [],
        }
        url = f"{self.endpoint}{menu.id}/form/"

        response = api_client.get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_respond(self, api_client):
        menu_response = baker.make(MenuResponse)
        response_dict = {
            "menu": menu_response.menu.id,
            "option": menu_response.option.id,
            "employee": menu_response.employee,
            "customization": menu_response.customization,
        }
        url = f"{self.endpoint}{menu_response.menu.id}/respond/"

        response = api_client.post(url, response_dict, format="json")

        assert response.status_code == 200
        assert MenuResponse.objects.all().count() == 2
