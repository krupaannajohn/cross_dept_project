# Generated by Django 4.2.5 on 2025-04-02 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_dept_app', '0003_remove_candidate_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.CharField(choices=[('Reached Out', 'Reached Out'), ('Consideration', 'Consideration'), ('Interview', 'Interview'), ('Offers', 'Offers'), ('Hire', 'Hire')], default=0, max_length=255),
            preserve_default=False,
        ),
    ]
