# Generated by Django 4.2.6 on 2023-10-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0015_remove_profile_profile_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_month',
            field=models.CharField(default=10, max_length=2),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_year',
            field=models.CharField(default=2023, max_length=4),
        ),
    ]
