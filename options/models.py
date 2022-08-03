from typing import Sequence, Union

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from options.constants import CONVERTER, FILE, STR, TYPE_CHOICES
from options.helpers import UploadToDir, convert_value
from options.managers import OptionManager, UserOptionManager


class BaseOption(models.Model):
    """Base model for system options and configurations."""

    name = models.CharField(
        verbose_name=_("parameter name"), max_length=255, unique=True, db_index=True
    )
    public_name = models.CharField(
        verbose_name=_("public name of the parameter"),
        max_length=255,
        unique=False,
        blank=True,
        db_index=True,
    )
    help_text = models.TextField(verbose_name=_("help text"), blank=True, null=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=STR)
    value = models.CharField(
        null=True, blank=True, default=None, max_length=256, verbose_name=_("value")
    )
    file = models.FileField(
        upload_to=UploadToDir("options", random_name=True), null=True, blank=True
    )
    is_list = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.public_name}"

    def get_value(self) -> Union[int, str, float, Sequence]:
        """Gets the value with the proper type. If the type is not
        valid it would return the default value for the field, to avoid
        problems with manual database modifications.
        """
        # If the option is a file, returns the URL of the file
        if self.type == FILE and self.file is not None:
            return self.file.url
        if not self.is_list:
            return convert_value(self.value, self.type)
        else:
            values = self.value.split(",")
            return [convert_value(value, self.type) for value in values]

    def clean(self) -> None:
        """Calls to the converter to check the type conversion. Added exception
        for lists, to check all values.
        """
        try:
            values = [self.value] if not self.is_list else self.value.split(",")
            [CONVERTER.get(self.type, str)(value) for value in values]
        except ValueError:
            raise ValidationError(_("Invalid value for this type."))
        # Default public name
        if not self.public_name:
            self.public_name = self.name

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Option(BaseOption):
    """System options and configurations."""

    objects = OptionManager()

    class Meta:
        ordering = ["public_name"]
        swappable = "SIMPLE_OPTIONS_OPTION_MODEL"


class UserOption(BaseOption):
    """Custom option for a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="options", on_delete=models.CASCADE
    )
    name = models.CharField(_("parameter name"), max_length=255)

    objects = UserOptionManager()

    class Meta:
        unique_together = ["user", "name"]
        ordering = ["public_name"]
        swappable = "SIMPLE_OPTIONS_USER_OPTION_MODEL"
