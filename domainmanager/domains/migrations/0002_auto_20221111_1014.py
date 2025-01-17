# Generated by Django 3.2 on 2022-11-11 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[(1, 'Pending'), (2, 'Verified'), (3, 'Disabled'), (4, 'Deleted')], max_length=255),
        ),
        migrations.AlterField(
            model_name='domain',
            name='source_type',
            field=models.CharField(choices=[(1, 'DNS'), (2, 'DB'), (3, 'Mirror')], max_length=255),
        ),
        migrations.AlterField(
            model_name='domain',
            name='status',
            field=models.CharField(choices=[(1, 'Pending'), (2, 'Verified'), (3, 'Disabled'), (4, 'Deleted')], max_length=255),
        ),
    ]
