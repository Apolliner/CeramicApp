# Generated by Django 3.1.6 on 2021-09-01 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CeramicApp', '0003_auto_20210829_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='language',
            field=models.ForeignKey(default='en', on_delete=django.db.models.deletion.PROTECT, to='CeramicApp.language'),
        ),
    ]