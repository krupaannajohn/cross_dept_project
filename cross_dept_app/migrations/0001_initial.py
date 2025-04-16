# Generated by Django 4.2.5 on 2025-04-01 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('experience', models.FloatField()),
                ('company', models.CharField(max_length=100)),
                ('current_designation', models.CharField(max_length=250)),
                ('current_ctc', models.CharField(max_length=250)),
                ('expected_ctc', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('Reached Out', 'Reached Out'), ('Consideration', 'Consideration'), ('Interview', 'Interview'), ('Offers', 'Offers'), ('Hire', 'Hire')], max_length=255)),
                ('phone_no', models.CharField(max_length=15)),
                ('source', models.CharField(choices=[('Naukri', 'Naukri'), ('Linkedin', 'Linkedin'), ('Employee Referral', 'Employee Referral')], max_length=50)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisition_no', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentFunnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(max_length=50)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funnel_stages', to='cross_dept_app.candidate')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='requisition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='cross_dept_app.requisition'),
        ),
    ]
