# Generated by Django 5.1.6 on 2025-03-08 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdocument',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
