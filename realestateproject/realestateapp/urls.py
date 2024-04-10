"""realestatproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from .views import save_break, user_login,delete_lead_view, user_logout, dashboard,create_custom_follow_up, assign_leads, myprofile, analysis, lead_analysis, my_attendance, inbox,export_lead_report

from .views import agent_reports, agent_performance_report, agent_attendance_report, export_agent_attendance, export_agent_reports, teamleader_reports, teamleader_performance_report, teamleader_attendance_report, export_teamleader_attendance, export_teamleader_reports

# Views for TeamLeader model
from .views import TeamLeaderListView, TeamLeaderCreateView, TeamLeaderUpdateView, TeamLeaderDeleteView, TeamLeaderAttendanceListView

# Views for Agent model
from .views import AgentListView, AgentCreateView, AgentUpdateView, AgentDeleteView, AgentAttendanceListView

# Views for Lead model
from .views import LeadListView, LeadCreateView, LeadUpdateView, LeadTransferListView, BulkLeadUpdateView,LeadFollowUpHistoryView

# Views for Contact model
from .views import ContactListView, ContactCreateView, ContactUpdateView, ContactDeleteView, UpdateContactNotesView

# Views for Task model
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,agent_sales_view,agent_update_target,team_leader_update_target

# Views for Marketing model
from .views import MarketingListView, MarketingCreateView, MarketingUpdateView, MarketingDeleteView,lead_reminder


# Views for Complaint model
from .views import ComplaintListView, ComplaintCreateView, ComplaintUpdateView, ComplaintDeleteView,backup_database,update_verify_request

# Views for Calendar model
from .views import CalendarListView, CalendarCreateView, CalendarUpdateView, CalendarDeleteView,clear_lead_reminders,update_verifed

# Views for PaidCustomer model
from .views import PaidCustomerListView, PaidCustomerCreateView, PaidCustomerUpdateView, PaidCustomerDeleteView,update_break_status

from realestateproject import settings


urlpatterns = [
    path('backup/', backup_database, name='backup_database'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('my_attendance/', my_attendance, name='my_attendance'),
    path('team_leader_profile/', myprofile, name='team_leader_profile'),
    path('create_custom_follow_up/', create_custom_follow_up, name='create_custom_follow_up'),
    path('lead_follow_up_history/<int:pk>/', LeadFollowUpHistoryView, name='lead_follow_up_history'),
    path('leads/assign/', assign_leads, name='assign_leads'),
    path('leads/delete/<int:lead_id>/', delete_lead_view, name='delete_lead'),
    path('analysis/', analysis, name='analysis'),
    path('save_break/', save_break, name='save_break'),
    path('update_break_status/', update_break_status, name='update_break_status'),
    path('leads_analysis/', lead_analysis, name='leads_analysis'),
    path('inbox/', inbox, name='inbox'),

    path('agent_reports/', agent_reports, name='agent_reports'),
    path('agent_performance_report/<int:agent_id>/', agent_performance_report, name='agent_performance_report'),
    path('agent_attendance_report/<int:agent_id>/', agent_attendance_report, name='agent_attendance_report'),
    path('export_agent_attendance/<int:agent_id>/', export_agent_attendance, name='export_agent_attendance'),
    path('export_agent_reports/', export_agent_reports, name='export_agent_reports'),

    path('teamleader_reports/', teamleader_reports, name='teamleader_reports'),
    path('teamleader_performance_report/<int:teamleader_id>/', teamleader_performance_report, name='teamleader_performance_report'),
    path('teamleader_attendance_report/<int:teamleader_id>/', teamleader_attendance_report, name='teamleader_attendance_report'),
    path('export_teamleader_attendance/<int:teamleader_id>/', export_teamleader_attendance, name='export_teamleader_attendance'),
    path('export_teamleader_reports/', export_teamleader_reports, name='export_teamleader_reports'),
    path('agent_sales/', agent_sales_view, name='agent_sales'),

    path('team_leaders/update_target/<int:team_leader_id>/', team_leader_update_target, name='team_leader_update_target'),
    path('team_leader_attendances/', TeamLeaderAttendanceListView.as_view(), name='team_leader_attendance'),
    path('team_leaders/', TeamLeaderListView.as_view(), name='team_leader_list'),
    path('team_leaders/create/', TeamLeaderCreateView.as_view(), name='team_leader_create'),
    path('team_leaders/update/<int:pk>/', TeamLeaderUpdateView.as_view(), name='team_leader_update'),
    path('team_leaders/delete/<int:pk>/', TeamLeaderDeleteView.as_view(), name='team_leader_delete'),

    path('agent/update_target/<int:agent_id>/', agent_update_target, name='agent_update_target'),
    path('agent_attendances/', AgentAttendanceListView.as_view(), name='agent_attendance'),
    path('agents/', AgentListView.as_view(), name='agent_list'),
    path('agents/create/', AgentCreateView.as_view(), name='agent_create'),
    path('agents/update/<int:pk>/', AgentUpdateView.as_view(), name='agent_update'),
    path('agents/delete/<int:pk>/', AgentDeleteView.as_view(), name='agent_delete'),

    path('paidcustomers/', PaidCustomerListView.as_view(), name='paidcustomer_list'),
    path('paidcustomers/create/', PaidCustomerCreateView.as_view(), name='paidcustomer_create'),
    path('paidcustomers/update/<int:pk>/', PaidCustomerUpdateView.as_view(), name='paidcustomer_update'),
    path('paidcustomers/delete/<int:pk>/', PaidCustomerDeleteView.as_view(), name='paidcustomer_delete'),
    path('update_verify_request/<int:paidcustomer_id>/', update_verify_request, name='update_verify_request'),
    path('update_verifed/<int:paidcustomer_id>/', update_verifed, name='update_verifed'),


    path('complaint/', ComplaintListView.as_view(), name='complaint_list'),
    path('complaint/create/', ComplaintCreateView.as_view(), name='complaint_create'),
    path('complaint/update/<int:pk>/', ComplaintUpdateView.as_view(), name='complaint_update'),
    path('complaint/delete/<int:pk>/', ComplaintDeleteView.as_view(), name='complaint_delete'),

    path('leads/', LeadListView.as_view(), name='lead_list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead_create'),
    path('leads/update/<int:pk>/', LeadUpdateView.as_view(), name='lead_update'),
    path('bulk_lead_update/', BulkLeadUpdateView.as_view(), name='bulk_lead_update'),
    path('lead_transfers/', LeadTransferListView.as_view(), name='lead_transfer_list'),
    path('export_lead_report/', export_lead_report, name='export_lead_report'),
    path('lead_reminder/<int:pk>/', lead_reminder, name='lead_reminder'),
    path('clear_lead_reminders/<int:lead_id>/', clear_lead_reminders, name='clear_lead_reminders'),


    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact_create'),
    path('contacts/update/<int:pk>/', ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/delete/<int:pk>/', ContactDeleteView.as_view(), name='contact_delete'),
    path('update_contact_notes/', UpdateContactNotesView.as_view(), name='update_contact_notes'),

    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),

    path('marketings/', MarketingListView.as_view(), name='marketing_list'),
    path('marketings/create/', MarketingCreateView.as_view(), name='marketing_create'),
    path('marketings/update/<int:pk>/', MarketingUpdateView.as_view(), name='marketing_update'),
    path('marketings/delete/<int:pk>/', MarketingDeleteView.as_view(), name='marketing_delete'),

    path('calendar/', CalendarListView.as_view(), name='calendar_list'),
    path('calendar/create/', CalendarCreateView.as_view(), name='calendar_create'),
    path('calendar/update/<int:pk>/', CalendarUpdateView.as_view(), name='calendar_update'),
    path('calendar/delete/<int:pk>/', CalendarDeleteView.as_view(), name='calendar_delete'),

]