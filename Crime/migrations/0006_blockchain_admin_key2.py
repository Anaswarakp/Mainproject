# Generated by Django 4.0.3 on 2022-06-23 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crime', '0005_alter_evidence_ledger_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchain_admin',
            name='key2',
            field=models.CharField(default='null', max_length=200, null=True),
        ),
    ]
