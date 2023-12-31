# Generated by Django 4.2.6 on 2023-10-13 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0005_remove_logs_time_stamp_logs_date_logs_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logs',
            old_name='action',
            new_name='message',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='authority',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='break_time',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='salary',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.AddField(
            model_name='profile',
            name='login_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='login_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='logout_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='logout_time',
            field=models.TimeField(null=True),
        ),
    ]
