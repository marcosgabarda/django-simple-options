from django.utils.translation import ugettext_lazy as _

FLOAT, INT, STRING, FILE = (0, 1, 2, 3)
TYPE_CHOICES = (
    (FLOAT, _("Float")),
    (INT, _("Integer")),
    (STRING, _("String")),
    (FILE, _("File")),
)
CONVERTER = {INT: int, FLOAT: float, STRING: str, FILE: str}
