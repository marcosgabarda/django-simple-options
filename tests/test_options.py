from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from options import INT, FLOAT, STR
from options.models import Option, UserOption
from tests.factories import UserFactory, UserOptionFactory, OptionFactory


class OptionTests(TestCase):
    def test_default_options(self):
        value = Option.objects.get_value("default_option", default="other")
        self.assertEqual("default", value)

    def test_int_conversion_options(self):
        name = "int_option"
        OptionFactory(name=name, value="42", type=INT)
        value = Option.objects.get_value(name)
        self.assertIsInstance(value, int)
        self.assertEqual(42, value)

    def test_str_conversion_options(self):
        name = "string_option"
        OptionFactory(name=name, value="42")
        value = Option.objects.get_value(name)
        self.assertIsInstance(value, str)
        self.assertEqual("42", value)

    def test_float_conversion_options(self):
        name = "string_option"
        OptionFactory(name=name, value="42.5", type=FLOAT)
        value = Option.objects.get_value(name)
        self.assertIsInstance(value, float)
        self.assertAlmostEqual(42.5, value)

    def test_public(self):
        options = OptionFactory.create_batch(size=5, is_public=True)
        OptionFactory.create_batch(size=3, is_public=False)
        self.assertEqual(len(options), Option.objects.public().count())


class UserOptionTests(TestCase):
    def test_custom_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOption.objects.create(
            name=name, public_name=name, value=expected_value, type=STR, user=user
        )
        value = UserOption.objects.get_value(name, user=user, default="other")
        self.assertEqual(expected_value, value)


class OptionAPITests(APITestCase):
    def test_list_options(self):
        options = OptionFactory.create_batch(size=10)
        admin = UserFactory(is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get("/api/options/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1 + len(options), len(data))

    def test_list_options_no_staff(self):
        OptionFactory.create_batch(size=10)
        options = OptionFactory.create_batch(size=3, is_public=True)
        admin = UserFactory()
        self.client.force_authenticate(admin)
        response = self.client.get("/api/options/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(options), len(data))

    def test_cant_update_options_no_staff(self):
        OptionFactory.create_batch(size=10)
        options = OptionFactory.create_batch(size=3, is_public=True)
        admin = UserFactory()
        self.client.force_authenticate(admin)
        data = {"value": "dummy"}
        response = self.client.patch(
            f"/api/options/{options[0].pk}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_options_staff(self):
        OptionFactory.create_batch(size=10)
        options = OptionFactory.create_batch(size=3, is_public=True)
        admin = UserFactory(is_staff=True)
        self.client.force_authenticate(admin)
        data = {"value": "dummy"}
        response = self.client.patch(
            f"/api/options/{options[0].pk}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOptionFactory(name=name, value=expected_value, user=user, is_public=True)
        self.client.force_authenticate(user)
        response = self.client.get("/api/user-options/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1, len(data))

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1, len(data))

    def test_create_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        data = {"name": name, "value": expected_value}
        self.client.force_authenticate(user)
        response = self.client.post("/api/user-options/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, UserOption.objects.filter(user=user).count())

    def test_create_user_options_excluded(self):
        user = UserFactory()
        name = "secret_option"
        expected_value = "secret"
        data = {"name": name, "value": expected_value}
        self.client.force_authenticate(user)
        response = self.client.post("/api/user-options/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
