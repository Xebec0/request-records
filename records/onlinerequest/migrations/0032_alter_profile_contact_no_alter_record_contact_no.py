# Generated by Django 4.2.11 on 2024-05-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinerequest', '0031_record_contact_no_record_entry_year_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_no',
            field=models.IntegerField(default='09667614313', max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='contact_no',
            field=models.IntegerField(default='09667614313', max_length=64),
        ),
    ]
