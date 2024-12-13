# Generated by Django 5.1.4 on 2024-12-12 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0012_imagefeed'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectedObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_type', models.CharField(max_length=100)),
                ('confidence', models.FloatField()),
                ('location', models.CharField(max_length=255)),
                ('image_feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detected_objects', to='task1.imagefeed')),
            ],
        ),
    ]