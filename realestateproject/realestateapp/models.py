from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta


class CustomUser(AbstractUser):
    USER_ROLES = [
        (1, "Admin"),
        (2, "Team Leader"),
        (3, "Agent"),
    ]
    role = models.PositiveIntegerField(choices=USER_ROLES, default=1)
    


class AdminUser(models.Model):
    auth_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class TeamLeader(models.Model):
    auth_user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='teamleader')
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    profile_pic = models.ImageField(upload_to='employ_profile_pic', null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    joining_date = models.DateField()
    remarks = models.TextField(blank=True)
    sales_traget = models.CharField(blank=True,null=True,max_length=255)

    def __str__(self):
        return self.username


class Agent(models.Model):
    auth_user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='agent')
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    profile_pic = models.ImageField(upload_to='employ_profile_pic', null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    joining_date = models.DateField()
    sales_traget = models.CharField(blank=True,null=True,max_length=255)
    remarks = models.TextField(blank=True)
    team_leader = models.ForeignKey(
        TeamLeader, on_delete=models.CASCADE, related_name='agents')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new contact
        super().save(*args, **kwargs)
        if is_new:

            users = CustomUser.objects.all()

            # Create contact notifications for the selected users
            notifications = [ContactNotification(
                user=user, contact=self) for user in users]
            ContactNotification.objects.bulk_create(notifications)

    def __str__(self):
        return self.name


class ContactNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class CustomFollowUp(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lead(models.Model):
    LEAD_STATUSES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    )

    SOURCE_CHOICES = (
        ('internet', 'Via Internet'),
        ('email', 'Email Inquiry'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('walk_in', 'Walk-in Customer'),
        ('website', 'Website'),
    )

    date = models.DateField()
    name = models.CharField(max_length=100)
    contact_info = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name='lead_contact', null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=20, choices=LEAD_STATUSES)
    details = models.TextField()
    follow_up_actions = models.ForeignKey(
        CustomFollowUp, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(
        TeamLeader, on_delete=models.CASCADE, related_name='team_leader_leads', null=True)
    assigned_to_agents = models.ForeignKey(
        Agent, on_delete=models.CASCADE, blank=True, related_name='agent_leads', null=True)
    last_seen_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='seen_leads', blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new lead
        super().save(*args, **kwargs)
        if is_new:
            # Get all users except the currently logged-in user
            users = CustomUser.objects.all()

            # Create lead notifications for the selected users
            notifications = [LeadNotification(
                user=user, lead=self) for user in users]
            LeadNotification.objects.bulk_create(notifications)

    def __str__(self):
        return self.name

class LeadReminder(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='reminders')
    set_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True)
    reminder_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f'Reminder for {self.lead} on {self.reminder_date}'
    


class FollowUpHistory(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name='follow_up_history')
    follow_up_date = models.DateField()
    follow_up_time = models.TimeField()
    follow_up_actions = models.ForeignKey(
        CustomFollowUp, on_delete=models.CASCADE)
    notes = models.TextField()
    agent = models.ForeignKey(
        Agent, on_delete=models.SET_NULL, null=True, blank=True)
    team_leader = models.ForeignKey(
        TeamLeader, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.lead.name} - Follow-up on {self.follow_up_date} at {self.follow_up_time}"


class LeadNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class LeadTransfer(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name='lead_transfers')
    from_agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name='transferred_leads', null=True, blank=True)
    to_agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name='received_leads', null=True, blank=True)
    from_team_leader = models.ForeignKey(
        TeamLeader, on_delete=models.CASCADE, related_name='transferred_leads', null=True, blank=True)
    to_team_leader = models.ForeignKey(
        TeamLeader, on_delete=models.CASCADE, related_name='received_leads', null=True, blank=True)
    transfer_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new lead
        super().save(*args, **kwargs)
        if is_new:
            # Get all users except the currently logged-in user
            users = CustomUser.objects.all()

            # Create lead notifications for the selected users
            notifications = [LeadTransferNotification(
                user=user, lead_transfer=self) for user in users]
            LeadTransferNotification.objects.bulk_create(notifications)

    def __str__(self):
        return f"Lead Transfer - {self.lead.name}"


class LeadTransferNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lead_transfer = models.ForeignKey(LeadTransfer, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class Task(models.Model):
    TASK_TYPES = (
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('follow-up', 'Follow-up'),
        ('other', 'Other'),
    )

    TASK_PRIORITIES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )

    TASK_STATUSES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(max_length=100)
    date = models.DateField()
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=TASK_PRIORITIES)
    status = models.CharField(max_length=100, choices=TASK_STATUSES)
    description = models.TextField()
    related_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new task
        super().save(*args, **kwargs)
        if is_new:

            users = CustomUser.objects.all()

            # Create task notifications for the assigned users
            notifications = [TaskNotification(
                user=user, task=self) for user in users]
            TaskNotification.objects.bulk_create(notifications)

    def __str__(self):
        return self.name


class TaskNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)



class Complaint(models.Model):
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    related_contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True)
    complaint_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new task
        super().save(*args, **kwargs)
        if is_new:

            users = CustomUser.objects.all()

            # Create task notifications for the assigned users
            notifications = [ComplaintNotification(
                user=user, complaint=self) for user in users]
            ComplaintNotification.objects.bulk_create(notifications)


class ComplaintNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, null=True)
    seen = models.BooleanField(default=False)


class Marketing(models.Model):
    CAMPAIGN_TYPES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('social_media', 'Social Media'),
        ('other', 'Other'),
    )

    CAMPAIGN_OBJECTIVES = (
        ('lead_generation', 'Lead Generation'),
        ('brand_awareness', 'Brand Awareness'),
        ('sales_conversion', 'Sales Conversion'),
        ('other', 'Other'),
    )

    CAMPAIGN_STATUSES = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    )
    date = models.DateField()
    name = models.CharField(max_length=100)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    campaign_objective = models.CharField(
        max_length=20, choices=CAMPAIGN_OBJECTIVES)
    campaign_status = models.CharField(
        max_length=20, choices=CAMPAIGN_STATUSES)
    target_audience = models.TextField()
    campaign_budget = models.DecimalField(max_digits=10, decimal_places=2)
    campaign_channels = models.TextField()

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new marketing campaign
        super().save(*args, **kwargs)
        if is_new:
            # Get all users
            users = CustomUser.objects.all()

            # Create marketing notifications for all users
            notifications = [MarketingNotification(
                user=user, marketing=self) for user in users]
            MarketingNotification.objects.bulk_create(notifications)

    def __str__(self):
        return self.name


class MarketingNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    marketing = models.ForeignKey(Marketing, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class Calendar(models.Model):
    name = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    participants = models.TextField()
    description = models.TextField()
    reminders = models.TextField()
    related_contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new calendar event
        super().save(*args, **kwargs)
        if is_new:
            # Get all users
            users = CustomUser.objects.all()

            # Create calendar notifications for the selected users
            notifications = [CalendarNotification(
                user=user, calendar=self) for user in users]
            CalendarNotification.objects.bulk_create(notifications)

    def __str__(self):
        return f"{self.name}"


class CalendarNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class PaidCustomer(models.Model):
    PAYMENT_METHODS = (
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('G-pay', 'G-pay'),
        ('Phonepe', 'Phonepe'),
        ('other', 'Other'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )

    related_contact = models.IntegerField( null=True,)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,
                             related_name='paid_customers', null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(blank=True)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES)
    verified = models.BooleanField(default=False)
    verify_request = models.BooleanField(default=False)

    def agent_name(self):
        if self.lead and self.lead.assigned_to_agents:
            return f"{self.lead.assigned_to_agents.first_name} {self.lead.assigned_to_agents.last_name}"
        return "NO AGENT"

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if it's a new calendar event
        super().save(*args, **kwargs)
        if is_new:
            # Get all users
            users = CustomUser.objects.all()

            # Create calendar notifications for the selected users
            notifications = [PaidCustomerNotification(
                user=user, paidcustomer=self) for user in users]
            PaidCustomerNotification.objects.bulk_create(notifications)

    def __str__(self):
        return f"{self.contact.name} ({self.payment_date})"


class PaidCustomerNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paidcustomer = models.ForeignKey(PaidCustomer, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class AgentSales(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    count_leads = models.PositiveIntegerField(default=0)
    lead_conversion = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    lead_completed = models.PositiveIntegerField(default=0)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    sales_achievement = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"Sale by {self.agent.first_name}"



class TeamLeaderAttendance(models.Model):
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], default='Absent')
    working_place = models.CharField(
        max_length=20, choices=[('Office', 'Office'), ('Online', 'Online')])
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    leaves_taken = models.BooleanField(default=False)
    is_on_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_leader} - {self.date} ({self.status})"


class AgentAttendance(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], null=True)
    working_place = models.CharField(
        max_length=20, choices=[('Office', 'Office'), ('Online', 'Online')])
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    leaves_taken = models.BooleanField(default=False)
    is_on_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.agent} - {self.date} ({self.status})"


class Break(models.Model):
    ROLE_CHOICES = [
        ('AD', 'Admin'),
        ('TL', 'Team Leader'),
        ('AG', 'Agent'),
    ]
    username = models.CharField(max_length=150, default='N/A')
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='N/A')
    start_time = models.DateTimeField(blank=True, null=True)
    stop_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)


class TeamLeaderNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    team_leader = models.ForeignKey(
        TeamLeader, on_delete=models.CASCADE, related_name='notifications', null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for Team Leader: {self.team_leader} - Agent: {self.agent}"

    @receiver(post_save, sender=Agent)
    def create_team_leader_notification(sender, instance, created, **kwargs):
        if created:
            # Get the team leader of the agent
            team_leader = instance.team_leader

            # Create a notification for the team leader
            TeamLeaderNotification.objects.create(
                user=team_leader.auth_user,
                team_leader=team_leader,
                agent=instance,
                message=f"New agent : {instance.first_name} {instance.last_name} has Joined your team."
            )

    @receiver(post_save, sender=Task)
    def create_task_notification(sender, instance, created, **kwargs):
        if created:
            assigned_user = instance.assigned_to
            task_name = instance.name

            if assigned_user.role == 2:  # Team Leader
                team_leader = assigned_user.teamleader

                # Create a notification for the team leader
                TeamLeaderNotification.objects.create(
                    user=team_leader.auth_user,
                    team_leader=team_leader,
                    agent=None,  # No associated agent for team leader notifications
                    message=f"New task : {task_name} assigned to team leader {team_leader.first_name} {team_leader.last_name}."
                )
            if assigned_user.role == 3:  # Agent
                agent = assigned_user.agent
                team_leader = agent.team_leader

                # Create a notification for the team leader
                TeamLeaderNotification.objects.create(
                    user=agent.auth_user,
                    team_leader=team_leader,
                    agent=agent,
                    message=f"New task : {task_name} assigned to agent {agent.first_name} {agent.last_name}."
                )

    @receiver(post_save, sender=Calendar)
    def create_calendar_notification(sender, instance, created, **kwargs):
        if created:
            assigned_user = instance.assigned_to

            if assigned_user.role == 2:  # Team Leader
                team_leader = assigned_user.teamleader

                # Create a notification for the team leader
                TeamLeaderNotification.objects.create(
                    user=team_leader.auth_user,
                    team_leader=team_leader,
                    agent=None,  # No associated agent for team leader notifications
                    message=f"New task assigned to team leader : {team_leader.first_name} {team_leader.last_name}."
                )
            if assigned_user.role == 3:  # Agent
                agent = assigned_user.agent
                team_leader = agent.team_leader

                # Create a notification for the team leader
                TeamLeaderNotification.objects.create(
                    user=agent.auth_user,
                    team_leader=team_leader,
                    agent=agent,
                    message=f"New task assigned to agent : {agent.first_name} {agent.last_name}."
                )

    @receiver(post_save, sender=LeadTransfer)
    def team_leader_to_team_leader_notification(sender, instance, created, **kwargs):
        if created and instance.from_team_leader and instance.to_team_leader:
            # Create a notification for the from_team_leader
            team_leader = instance.from_team_leader
            TeamLeaderNotification.objects.create(
                user=team_leader.auth_user,
                team_leader=team_leader,
                message=f"Lead transfer: Lead '{instance.lead.name}' has been transferred from Team Leader '{instance.from_team_leader.first_name} {instance.from_team_leader.last_name}' to Team Leader '{instance.to_team_leader.first_name} {instance.to_team_leader.last_name}'."
            )
            team_leader = instance.to_team_leader
            # Create a notification for the to_team_leader
            TeamLeaderNotification.objects.create(
                user=team_leader.auth_user,
                team_leader=instance.to_team_leader,
                message=f"Lead transfer: Lead '{instance.lead.name}' has been transferred from Team Leader '{instance.from_team_leader.first_name} {instance.from_team_leader.last_name}' to Team Leader '{instance.to_team_leader.first_name} {instance.to_team_leader.last_name}'."
            )

    @receiver(post_save, sender=LeadTransfer)
    def agent_to_agent_notification(sender, instance, created, **kwargs):
        if created and instance.from_agent and instance.to_agent:
            # Create a notification for the from_agent
            agent = instance.from_agent
            TeamLeaderNotification.objects.create(
                user=agent.auth_user,
                team_leader=instance.from_agent.team_leader,
                agent=agent,
                message=f"Lead transfer: Lead '{instance.lead.name}' has been transferred from Agent '{instance.from_agent.first_name} {instance.from_agent.last_name}' to Agent '{instance.to_agent.first_name} {instance.to_agent.last_name}'."
            )
            agent = instance.to_agent
            # Create a notification for the to_agent
            TeamLeaderNotification.objects.create(
                user=agent.auth_user,
                team_leader=instance.to_agent.team_leader,
                agent=agent,
                message=f"Lead transfer: Lead '{instance.lead.name}' has been transferred from Agent '{instance.from_agent.first_name} {instance.from_agent.last_name}' to Agent '{instance.to_agent.first_name} {instance.to_agent.last_name}'."
            )

    @receiver(post_save, sender=Complaint)
    def create_complaint_notification(sender, instance, created, **kwargs):
        if created:
            assigned_user = instance.assigned_to

            if assigned_user.role == 2:  # Team Leader
                # Create a notification for the team leader
                TeamLeaderNotification.objects.create(
                    user=assigned_user,
                    team_leader=assigned_user.teamleader,
                    message=f"New complaint received from {instance.related_contact.name} is assigned to {assigned_user}."
                )
            elif assigned_user.role == 3:  # Agent
                # Create a notification for the agent
                TeamLeaderNotification.objects.create(
                    user=assigned_user,
                    team_leader=assigned_user.agent.team_leader,
                    agent=assigned_user.agent,
                    message=f"New complaint received for {instance.related_contact.name} is assigned to {assigned_user}."
                )
