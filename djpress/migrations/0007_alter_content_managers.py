# Generated by Django 5.0.4 on 2024-04-29 05:34

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djpress', '0006_alter_category_slug'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='content',
            managers=[
                ('post_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]