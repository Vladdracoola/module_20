# Generated by Django 5.1.4 on 2024-12-10 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0010_user_last_login'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]