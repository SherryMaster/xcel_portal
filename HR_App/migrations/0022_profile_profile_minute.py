# Generated by Django 4.2.6 on 2023-12-20 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0021_profile_is_logged_in_alter_profile_profile_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_minute',
            field=models.CharField(default=14, max_length=2),
        ),
    ]
