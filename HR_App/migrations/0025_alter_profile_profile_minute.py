# Generated by Django 4.2.6 on 2023-12-20 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0024_remove_profile_user_alter_profile_profile_minute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_minute',
            field=models.CharField(default=37, max_length=2),
        ),
    ]
