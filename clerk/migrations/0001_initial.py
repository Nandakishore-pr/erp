# Generated by Django 5.1.6 on 2025-02-25 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('time', models.TimeField(auto_now_add=True)),
                ('session', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon')], max_length=20)),
                ('status', models.CharField(default='Present', max_length=10)),
            ],
        ),
    ]
