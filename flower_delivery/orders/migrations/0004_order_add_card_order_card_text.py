# Generated by Django 5.1.3 on 2024-12-18 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_product_remove_order_quantity_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='add_card',
            field=models.BooleanField(default=False, verbose_name='Добавить открытку?'),
        ),
        migrations.AddField(
            model_name='order',
            name='card_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст открытки'),
        ),
    ]
