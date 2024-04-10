# Generated by Django 4.2.4 on 2023-09-07 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reminder_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='realestateapp.lead')),
            ],
        ),
    ]