# Generated by Django 4.1.7 on 2023-02-24 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='update_at',
            field=models.DateTimeField(null=True),
        ),
    ]
