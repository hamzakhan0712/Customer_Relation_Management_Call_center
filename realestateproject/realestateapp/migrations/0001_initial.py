# Generated by Django 4.2.4 on 2023-09-07 07:35

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.PositiveIntegerField(choices=[(1, 'Admin'), (2, 'Team Leader'), (3, 'Agent')], default=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('profile_pic', models.ImageField(null=True, upload_to='employ_profile_pic')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('joining_date', models.DateField()),
                ('sales_traget', models.CharField(blank=True, max_length=255, null=True)),
                ('remarks', models.TextField(blank=True)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='N/A', max_length=150)),
                ('role', models.CharField(choices=[('AD', 'Admin'), ('TL', 'Team Leader'), ('AG', 'Agent')], default='N/A', max_length=2)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('stop_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('event_date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('participants', models.TextField()),
                ('description', models.TextField()),
                ('reminders', models.TextField()),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('source', models.CharField(choices=[('internet', 'Via Internet'), ('email', 'Email Inquiry'), ('referral', 'Referral'), ('social_media', 'Social Media'), ('walk_in', 'Walk-in Customer'), ('website', 'Website')], max_length=100)),
                ('status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('converted', 'Converted'), ('lost', 'Lost')], max_length=20)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LeadTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_date', models.DateTimeField(auto_now_add=True)),
                ('from_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transferred_leads', to='realestateapp.agent')),
            ],
        ),
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('campaign_type', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline'), ('social_media', 'Social Media'), ('other', 'Other')], max_length=20)),
                ('campaign_objective', models.CharField(choices=[('lead_generation', 'Lead Generation'), ('brand_awareness', 'Brand Awareness'), ('sales_conversion', 'Sales Conversion'), ('other', 'Other')], max_length=20)),
                ('campaign_status', models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed')], max_length=20)),
                ('target_audience', models.TextField()),
                ('campaign_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('campaign_channels', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PaidCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer'), ('G-pay', 'G-pay'), ('Phonepe', 'Phonepe'), ('other', 'Other')], max_length=20)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('transaction_id', models.CharField(max_length=100)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('refunded', 'Refunded'), ('cancelled', 'Cancelled')], max_length=50)),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paid_customers', to='realestateapp.lead')),
                ('related_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_customers', to='realestateapp.contact')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('task_type', models.CharField(choices=[('call', 'Call'), ('meeting', 'Meeting'), ('email', 'Email'), ('follow-up', 'Follow-up'), ('other', 'Other')], max_length=20)),
                ('due_date', models.DateField()),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=100)),
                ('description', models.TextField()),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realestateapp.contact')),
            ],
        ),
        migrations.CreateModel(
            name='TeamLeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=128)),
                ('profile_pic', models.ImageField(null=True, upload_to='employ_profile_pic')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('joining_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('sales_traget', models.CharField(blank=True, max_length=255, null=True)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teamleader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamLeaderNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realestateapp.agent')),
                ('team_leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='realestateapp.teamleader')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamLeaderAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], default='Absent', max_length=20)),
                ('working_place', models.CharField(choices=[('Office', 'Office'), ('Online', 'Online')], max_length=20)),
                ('login_time', models.DateTimeField(blank=True, null=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('leaves_taken', models.BooleanField(default=False)),
                ('is_on_break', models.BooleanField(default=False)),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.teamleader')),
            ],
        ),
        migrations.CreateModel(
            name='TaskNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaidCustomerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('paidcustomer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.paidcustomer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarketingNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('marketing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.marketing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeadTransferNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('lead_transfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.leadtransfer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='leadtransfer',
            name='from_team_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transferred_leads', to='realestateapp.teamleader'),
        ),
        migrations.AddField(
            model_name='leadtransfer',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_transfers', to='realestateapp.lead'),
        ),
        migrations.AddField(
            model_name='leadtransfer',
            name='to_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_leads', to='realestateapp.agent'),
        ),
        migrations.AddField(
            model_name='leadtransfer',
            name='to_team_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_leads', to='realestateapp.teamleader'),
        ),
        migrations.CreateModel(
            name='LeadNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.lead')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_leader_leads', to='realestateapp.teamleader'),
        ),
        migrations.AddField(
            model_name='lead',
            name='assigned_to_agents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_leads', to='realestateapp.agent'),
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_contact', to='realestateapp.contact'),
        ),
        migrations.AddField(
            model_name='lead',
            name='follow_up_actions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realestateapp.customfollowup'),
        ),
        migrations.AddField(
            model_name='lead',
            name='last_seen_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seen_leads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FollowUpHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_up_date', models.DateField()),
                ('follow_up_time', models.TimeField()),
                ('notes', models.TextField()),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realestateapp.agent')),
                ('follow_up_actions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.customfollowup')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_up_history', to='realestateapp.lead')),
                ('team_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realestateapp.teamleader')),
            ],
        ),
        migrations.CreateModel(
            name='ContactNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.contact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('complaint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realestateapp.complaint')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='complaint',
            name='related_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realestateapp.contact'),
        ),
        migrations.CreateModel(
            name='CalendarNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.calendar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='calendar',
            name='related_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='realestateapp.contact'),
        ),
        migrations.CreateModel(
            name='AgentSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('count_leads', models.PositiveIntegerField(default=0)),
                ('lead_conversion', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('lead_completed', models.PositiveIntegerField(default=0)),
                ('sale_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sales_achievement', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.agent')),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.teamleader')),
            ],
        ),
        migrations.CreateModel(
            name='AgentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], max_length=20, null=True)),
                ('working_place', models.CharField(choices=[('Office', 'Office'), ('Online', 'Online')], max_length=20)),
                ('login_time', models.DateTimeField(blank=True, null=True)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('leaves_taken', models.BooleanField(default=False)),
                ('is_on_break', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestateapp.agent')),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='realestateapp.teamleader'),
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
