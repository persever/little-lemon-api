# Generated by Django 5.0 on 2023-12-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0005_alter_category_options_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='price',
            new_name='total',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=255),
        ),
    ]