# Generated by Django 4.2.4 on 2023-09-09 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='image',
        ),
        migrations.AddField(
            model_name='property',
            name='images',
            field=models.JSONField(null=True),
        ),
    ]
