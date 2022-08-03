from typing import Dict, Type

from django.utils.translation import gettext_lazy as _

FLOAT, INT, STR, FILE = (0, 1, 2, 3)
TYPE_CHOICES = (
    (FLOAT, _("Float")),
    (INT, _("Integer")),
    (STR, _("String")),
    (FILE, _("File")),
)
CONVERTER: Dict[int, Type] = {INT: int, FLOAT: float, STR: str, FILE: str}
