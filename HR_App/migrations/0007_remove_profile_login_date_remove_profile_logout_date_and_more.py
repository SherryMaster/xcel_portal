# Generated by Django 4.2.6 on 2023-10-13 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0006_rename_action_logs_message_remove_profile_authority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='login_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='logout_date',
        ),
        migrations.AlterField(
            model_name='profile',
            name='login_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='logout_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
