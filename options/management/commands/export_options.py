import json

from django.core.management import BaseCommand

from options.models import Option


class Command(BaseCommand):
    help = "Export current options to JSON format."

    def handle(self, *args, **options):
        export = dict()
        for option in Option.objects.all():
            export[option.name] = {
                "value": option.value,
                "type": option.type,
                "public_name": option.public_name,
            }
        self.stdout.write(json.dumps(export, indent=4, sort_keys=True))
