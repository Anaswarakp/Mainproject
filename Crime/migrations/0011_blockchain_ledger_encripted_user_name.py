# Generated by Django 4.0.3 on 2022-06-23 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crime', '0010_alter_blockchain_ledger_encripted_blockchain_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchain_ledger_encripted',
            name='user_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
