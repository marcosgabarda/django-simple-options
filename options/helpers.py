import six

from options import INT, FLOAT, STRING, CONVERTER


def convert_value(value, value_type):
    """Converts the given value to the given type."""
    default_values = {INT: 0, FLOAT: 1.0, STRING: ""}
    try:
        option_value = CONVERTER.get(value_type, six.text_type)(value)
    except ValueError:
        option_value = default_values.get(value_type)
    return option_value
