# Generated by Django 4.0.3 on 2022-06-20 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crime', '0004_evidence_police_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidence',
            name='ledger_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Crime.complaint'),
        ),
    ]
