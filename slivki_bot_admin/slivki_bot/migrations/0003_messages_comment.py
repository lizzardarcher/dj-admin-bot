# Generated by Django 3.2.6 on 2021-08-23 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slivki_bot', '0002_messages_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='comment',
            field=models.TextField(default='', max_length=4000),
        ),
    ]
