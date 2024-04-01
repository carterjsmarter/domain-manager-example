# Generated by Django 3.2 on 2022-11-11 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0003_auto_20221111_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='domain_cap',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('1', 'Pending'), ('2', 'Verified'), ('3', 'Disabled'), ('4', 'Deleted')], default='1', max_length=255),
        ),
        migrations.AlterField(
            model_name='domain',
            name='source_type',
            field=models.CharField(choices=[('1', 'DNS'), ('2', 'DB'), ('3', 'Mirror')], default='1', max_length=255),
        ),
        migrations.AlterField(
            model_name='domain',
            name='status',
            field=models.CharField(choices=[('1', 'Pending'), ('2', 'Verified'), ('3', 'Disabled'), ('4', 'Deleted')], default='1', max_length=255),
        ),
    ]
