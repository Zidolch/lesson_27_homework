# Generated by Django 4.1.5 on 2023-01-24 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_location_options_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='location_id',
            new_name='locations',
        ),
    ]
