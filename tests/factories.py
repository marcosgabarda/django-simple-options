from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation
from factory.fuzzy import FuzzyText

from options import STR
from options.models import Option, UserOption


class UserFactory(DjangoModelFactory):

    username = Faker("email")

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(extra_kwargs={})
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class OptionFactory(DjangoModelFactory):
    name = FuzzyText()
    public_name = FuzzyText()
    type = STR

    class Meta:
        model = Option


class UserOptionFactory(DjangoModelFactory):
    name = FuzzyText()
    public_name = FuzzyText()
    type = STR

    class Meta:
        model = UserOption
