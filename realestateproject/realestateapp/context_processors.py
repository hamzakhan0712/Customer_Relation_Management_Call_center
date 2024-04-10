from .models import (TeamLeader, Lead, LeadNotification, ContactNotification, TaskNotification, MarketingNotification,
                     CalendarNotification, Agent, TeamLeaderNotification, ComplaintNotification, PaidCustomerNotification,
                     LeadTransferNotification)
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def notifications(request):
    if request.user.is_authenticated:
        current_user = request.user
        unseen_leads_count = LeadNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_contacts_count = ContactNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_tasks_count = TaskNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_marketing_count = MarketingNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_calendar_count = CalendarNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_complaints_count = ComplaintNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_paidcustomer_count = PaidCustomerNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_lead_transfer_count = LeadTransferNotification.objects.filter(
            user=current_user, seen=False).count()
        unseen_team_leader_count = TeamLeaderNotification.objects.filter(
            user=current_user, seen=False).count()

        return {
            'unseen_leads_count': unseen_leads_count,
            'unseen_contacts_count': unseen_contacts_count,
            'unseen_tasks_count': unseen_tasks_count,
            'unseen_marketing_count': unseen_marketing_count,
            'unseen_calendar_count': unseen_calendar_count,
            'unseen_complaints_count': unseen_complaints_count,
            'unseen_paidcustomer_count': unseen_paidcustomer_count,
            'unseen_lead_transfer_count': unseen_lead_transfer_count,
            'unseen_team_leader_count': unseen_team_leader_count
        }

    else:
        return {}
