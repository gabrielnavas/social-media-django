# Generated by Django 4.1.7 on 2023-02-21 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_profile_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
