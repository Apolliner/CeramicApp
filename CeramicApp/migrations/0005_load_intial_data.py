from django.db import migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    call_command('loaddata', 'initial_data.json')


class Migration(migrations.Migration):

    dependencies = [
        ('CeramicApp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]