
import django.db.models.deletion
import django_quill.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0005_milestone_category'),
        ('Users', '0009_alter_freelancerprofile_skills_alter_skill_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='category',
            field=models.CharField(choices=[('normal', 'Normal'), ('planning', 'Planning'), ('development', 'Development'), ('review', 'Review'), ('delivery', 'Delivery'), ('documentation', 'Documentation')], default='development', max_length=20),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', django_quill.fields.QuillField()),
                ('due_date', models.DateField()),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=15)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='task_files/')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='Users.freelancerprofile')),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='Projects.milestone')),
            ],
        ),
    ]
