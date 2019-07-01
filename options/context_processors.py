from options.models import Option


def options(request):
    """Context processor that adds options to the template context."""
    return {option.name: option.get_value() for option in Option.objects.all()}
