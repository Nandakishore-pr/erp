# Generated by Django 5.1.6 on 2025-03-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panchayath_ad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admindocument',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
