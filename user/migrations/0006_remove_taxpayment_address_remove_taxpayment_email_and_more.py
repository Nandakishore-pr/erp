# Generated by Django 5.1.6 on 2025-03-19 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_taxpayment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxpayment',
            name='address',
        ),
        migrations.RemoveField(
            model_name='taxpayment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='taxpayment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='taxpayment',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='taxpayment',
            name='ward',
        ),
    ]
