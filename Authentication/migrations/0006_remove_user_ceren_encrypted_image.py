# Generated by Django 4.1.1 on 2022-10-27 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0005_user_ceren_encrypted_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_ceren',
            name='Encrypted_image',
        ),
    ]
