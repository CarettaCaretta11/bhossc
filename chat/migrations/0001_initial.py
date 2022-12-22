# Generated by Django 3.2.8 on 2022-12-21 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PmMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('sender', models.CharField(max_length=255, null=True)),
                ('room', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
