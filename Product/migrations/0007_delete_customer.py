# Generated by Django 2.2.7 on 2021-06-08 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_remove_order_customer_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
