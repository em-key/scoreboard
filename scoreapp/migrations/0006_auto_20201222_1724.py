# Generated by Django 3.1.4 on 2020-12-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreapp', '0005_auto_20201222_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
