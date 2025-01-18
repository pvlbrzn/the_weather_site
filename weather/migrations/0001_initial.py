# Generated by Django 4.2.18 on 2025-01-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temp', models.FloatField()),
                ('description', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
