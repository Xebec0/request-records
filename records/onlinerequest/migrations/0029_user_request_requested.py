# Generated by Django 4.2.11 on 2024-05-01 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinerequest', '0028_alter_user_request_uploads'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_request',
            name='requested',
            field=models.CharField(default='', max_length=256),
        ),
    ]
