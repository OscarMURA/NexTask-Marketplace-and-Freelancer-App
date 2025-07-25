# Generated by Django 5.1 on 2024-11-05 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0005_remove_recurringpayment_client_and_more'),
        ('Projects', '0014_merge_20241020_1656'),
        ('Users', '0011_alter_certification_certification_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodicPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='weekly', max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('next_payment_date', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_payments', to='Users.clientprofile')),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_payments', to='Users.freelancerprofile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_payments', to='Projects.project')),
            ],
        ),
    ]
