# Generated by Django 4.2.2 on 2023-07-11 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine_main', '0002_alter_item_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='borrowed',
            field=models.BooleanField(default=False),
        ),
    ]