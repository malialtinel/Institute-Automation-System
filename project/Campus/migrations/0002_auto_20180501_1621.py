# Generated by Django 2.0.4 on 2018-05-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='place',
            field=models.CharField(choices=[('101', '101'), ('102', '102'), ('103', '103')], max_length=15, verbose_name='Place'),
        ),
    ]
