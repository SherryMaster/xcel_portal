# Generated by Django 5.0 on 2024-01-04 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0030_remove_performance_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='break_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='break_start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
