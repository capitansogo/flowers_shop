# Generated by Django 5.0 on 2023-12-18 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.RenameModel(
            old_name='Services',
            new_name='Service',
        ),
        migrations.RenameModel(
            old_name='Supplies',
            new_name='Supplie',
        ),
        migrations.RenameModel(
            old_name='SuppliesItem',
            new_name='SupplieItem',
        ),
        migrations.RenameModel(
            old_name='Types_products',
            new_name='Types_product',
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]
