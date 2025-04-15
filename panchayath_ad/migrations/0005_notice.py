# Generated by Django 5.1.6 on 2025-04-13 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panchayath_ad', '0004_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='notices/')),
                ('recipient', models.CharField(choices=[('public', 'Public'), ('clerks', 'Clerks'), ('engineers', 'Engineers'), ('everyone', 'Everyone')], max_length=20)),
                ('date', models.DateField()),
            ],
        ),
    ]
