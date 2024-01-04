# Generated by Django 5.0 on 2024-01-01 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0027_alter_performance_break_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='break_end_time',
            field=models.TimeField(blank=True, default=datetime.time(18, 38, 59, 761709), null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='break_start_time',
            field=models.TimeField(blank=True, default=datetime.time(18, 38, 59, 761709), null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2024, 1, 1), null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='end_time',
            field=models.TimeField(blank=True, default=datetime.time(18, 38, 59, 761709), null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='login_time',
            field=models.TimeField(blank=True, default=datetime.time(18, 38, 59, 761709), null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='start_time',
            field=models.TimeField(blank=True, default=datetime.time(18, 38, 59, 761709), null=True),
        ),
    ]