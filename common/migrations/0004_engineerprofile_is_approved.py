# Generated by Django 5.1.6 on 2025-03-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_engineerprofile_license_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineerprofile',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
