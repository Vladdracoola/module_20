# Generated by Django 5.1.3 on 2024-11-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=99)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=99)),
                ('size', models.DecimalField(decimal_places=2, max_digits=99)),
                ('description', models.TextField()),
                ('age_limited', models.BooleanField(default=None)),
            ],
        ),
    ]
