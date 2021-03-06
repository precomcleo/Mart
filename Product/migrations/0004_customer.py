# Generated by Django 2.2.7 on 2021-06-07 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_order_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='顧客id')),
                ('is_vip', models.BooleanField(default=False, verbose_name='True => 是VIP/ False =>非VIP')),
            ],
        ),
    ]
