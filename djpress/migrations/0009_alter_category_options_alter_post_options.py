# Generated by Django 5.0.4 on 2024-05-02 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djpress', '0001_squashed_0008_rename_content_post_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
    ]
