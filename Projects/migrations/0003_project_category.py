# Generated by Django 5.1.1 on 2024-09-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(choices=[('web_development', 'Web Development'), ('mobile_app_development', 'Mobile App Development'), ('graphic_design', 'Graphic Design'), ('content_writing', 'Content Writing'), ('digital_marketing', 'Digital Marketing'), ('seo', 'SEO'), ('video_editing', 'Video Editing'), ('data_entry', 'Data Entry'), ('translation', 'Translation Services'), ('customer_support', 'Customer Support'), ('software_development', 'Software Development'), ('it_networking', 'IT & Networking'), ('ecommerce', 'E-commerce Development'), ('virtual_assistance', 'Virtual Assistance'), ('project_management', 'Project Management'), ('accounting_finance', 'Accounting & Finance'), ('legal_consulting', 'Legal Consulting')], default='web_development', max_length=50),
        ),
    ]
