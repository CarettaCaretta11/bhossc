# Generated by Django 4.1.3 on 2023-01-22 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_reglinka_reglink_reglink'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reglink',
            old_name='reglink',
            new_name='reglinka',
        ),
    ]
