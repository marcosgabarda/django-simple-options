import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from options import FLOAT, INT, STR
from options.models import Option, UserOption
from tests.factories import OptionFactory, UserFactory, UserOptionFactory


@pytest.mark.django_db
class OptionTests:
    def test_default_options(self):
        value = Option.objects.get_value("default_option", default="other")
        assert value == "default"

    def test_int_conversion_options(self):
        name = "int_option"
        OptionFactory(name=name, value="42", type=INT)
        value = Option.objects.get_value(name)
        assert isinstance(value, int)
        assert value == 42

    def test_str_conversion_options(self):
        name = "string_option"
        OptionFactory(name=name, value="42")
        value = Option.objects.get_value(name)
        assert isinstance(value, str)
        assert value == "42"

    def test_float_conversion_options(self):
        name = "float_option"
        OptionFactory(name=name, value="42.5", type=FLOAT)
        value = Option.objects.get_value(name)
        assert isinstance(value, float)
        assert value == 42.5

    def test_public(self):
        options = OptionFactory.create_batch(size=5, is_public=True)
        OptionFactory.create_batch(size=3, is_public=False)
        assert Option.objects.public().count() == len(options)


@pytest.mark.django_db
class UserOptionTests:
    def test_custom_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOption.objects.create(
            name=name, public_name=name, value=expected_value, type=STR, user=user
        )
        value = UserOption.objects.get_value(name, user=user, default="other")
        assert value == expected_value


class OptionAPITests(APITestCase):
    def test_list_options(self):
        options = OptionFactory.create_batch(size=10)
        admin = UserFactory(is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get("/api/options/", format="json")
        assert status.HTTP_200_OK == response.status_code
        data = response.json()
        assert len(data) == 1 + len(options)

    def test_list_options_no_staff(self):
        OptionFactory.create_batch(size=10)
        options = OptionFactory.create_batch(size=3, is_public=True)
        admin = UserFactory()
        self.client.force_authenticate(admin)
        response = self.client.get("/api/options/", format="json")
        assert status.HTTP_200_OK == response.status_code
        data = response.json()
        assert len(data) == len(options)

    def test_cant_update_options_no_staff(self):
        OptionFactory.create_batch(size=10)
        options = OptionFactory.create_batch(size=3, is_public=True)
        admin = UserFactory()
        self.client.force_authenticate(admin)
        data = {"value": "dummy"}
        response = self.client.patch(
            f"/api/options/{options[0].pk}/", data=data, format="json"
        )
        assert status.HTTP_403_FORBIDDEN == response.status_code

    def test_can_update_options_staff(self):
        OptionFactory.create_batch(size=10)
        options = OptionFactory.create_batch(size=3, is_public=True)
        admin = UserFactory(is_staff=True)
        self.client.force_authenticate(admin)
        data = {"value": "dummy"}
        response = self.client.patch(
            f"/api/options/{options[0].pk}/", data=data, format="json"
        )
        assert status.HTTP_200_OK == response.status_code

    def test_list_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOptionFactory(name=name, value=expected_value, user=user, is_public=True)
        self.client.force_authenticate(user)
        response = self.client.get("/api/user-options/", format="json")
        assert status.HTTP_200_OK == response.status_code
        data = response.json()
        assert len(data) == 1

    def test_list_user_options_with_exclude(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOptionFactory(
            name="secret_option", value="secret", user=user, is_public=True
        )
        UserOptionFactory(name=name, value=expected_value, user=user, is_public=True)
        self.client.force_authenticate(user)
        response = self.client.get("/api/user-options/", format="json")
        assert status.HTTP_200_OK == response.status_code
        data = response.json()
        assert len(data) == 1

    def test_create_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        data = {"name": name, "value": expected_value}
        self.client.force_authenticate(user)
        response = self.client.post("/api/user-options/", data=data, format="json")
        assert status.HTTP_201_CREATED == response.status_code
        assert UserOption.objects.filter(user=user).count() == 1

    def test_create_user_options_excluded(self):
        user = UserFactory()
        name = "secret_option"
        expected_value = "secret"
        data = {"name": name, "value": expected_value}
        self.client.force_authenticate(user)
        response = self.client.post("/api/user-options/", data=data, format="json")
        assert status.HTTP_400_BAD_REQUEST == response.status_code
