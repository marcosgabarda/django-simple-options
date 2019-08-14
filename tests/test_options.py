from django.test import override_settings, TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from tests.test_settings import TEST_SETTINGS
from tests.factories import UserFactory, UserOptionFactory, OptionFactory
from options import INT, FLOAT, STRING
from options.models import Option, UserOption


@override_settings(**TEST_SETTINGS)
class OptionTests(TestCase):
    def test_default_options(self):
        value = Option.objects.get_value("default_option", default="ohter")
        self.assertEqual("default", value)

    def test_int_conversion_options(self):
        name = "int_option"
        option = OptionFactory(name=name, value="42", type=INT)
        value = Option.objects.get_value(name)
        self.assertIsInstance(value, int)
        self.assertEqual(42, value)

    def test_str_conversion_options(self):
        name = "string_option"
        option = OptionFactory(name=name, value="42")
        value = Option.objects.get_value(name)
        self.assertIsInstance(value, str)
        self.assertEqual("42", value)

    def test_float_conversion_options(self):
        name = "string_option"
        option = OptionFactory(name=name, value="42.5", type=FLOAT)
        value = Option.objects.get_value(name)
        self.assertIsInstance(value, float)
        self.assertAlmostEqual(42.5, value)


@override_settings(**TEST_SETTINGS)
class UserOptionTests(TestCase):
    def test_custom_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOption.objects.create(
            name=name, public_name=name, value=expected_value, type=STRING, user=user
        )
        value = UserOption.objects.get_value(name, user=user, default="ohter")
        self.assertEqual(expected_value, value)


@override_settings(**TEST_SETTINGS)
class OptionAPITests(APITestCase):
    def test_list_options(self):
        admin = UserFactory(is_staff=True)
        self.client.force_authenticate(admin)
        response = self.client.get("/api/options/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1, len(data))

    def test_list_user_options(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOptionFactory(name=name, value=expected_value, user=user)
        self.client.force_authenticate(user)
        response = self.client.get("/api/user-options/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1, len(data))

    def test_list_user_options_with_exclude(self):
        user = UserFactory()
        name = "default_option"
        expected_value = "user default"
        UserOptionFactory(name="secret_option", value="secret", user=user)
        UserOptionFactory(name=name, value=expected_value, user=user)
        self.client.force_authenticate(user)
        response = self.client.get("/api/user-options/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(1, len(data))
