# Generated by Django 4.2.5 on 2025-04-02 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_dept_app', '0002_remove_candidate_current_ctc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='status',
        ),
        migrations.AlterField(
            model_name='candidate',
            name='requisition_no',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='source',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
