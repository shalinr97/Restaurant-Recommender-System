# Generated by Django 2.1.7 on 2019-04-19 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restro', '0008_auto_20190324_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant_atrributes',
            name='restaurant',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='Restaurant_atrributes',
        ),
    ]
