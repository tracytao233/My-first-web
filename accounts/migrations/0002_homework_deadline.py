# Generated by Django 2.0.13 on 2020-04-14 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]