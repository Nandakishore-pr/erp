# Generated by Django 5.1.6 on 2025-04-12 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_complaint_name_remove_complaint_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
