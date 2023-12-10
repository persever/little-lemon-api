# Generated by Django 5.0 on 2023-12-10 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0003_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='inventory',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='featured',
            field=models.BooleanField(db_index=True, default=False),
            preserve_default=False,
        ),
    ]