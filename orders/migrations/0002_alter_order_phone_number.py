# Generated by Django 5.0.1 on 2024-02-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=22, verbose_name='Номер телефона'),
        ),
    ]
