# Generated by Django 5.1.1 on 2024-12-18 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_add_card_order_card_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={},
        ),
        migrations.RemoveField(
            model_name='order',
            name='comment',
        ),
    ]
