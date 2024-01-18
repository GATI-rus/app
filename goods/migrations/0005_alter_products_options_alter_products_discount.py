# Generated by Django 5.0.1 on 2024-01-18 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_alter_products_category_alter_products_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ('id',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='products',
            name='discount',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=4, verbose_name='Скидка в %'),
        ),
    ]
