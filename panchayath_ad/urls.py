from django.urls import path
from . import views

urlpatterns = [
    
    path('admin1/', views.home, name='admindashboard'),
    path('manage/',views.manage, name='manage'),
    path('admin_engineer/',views.admin_engineer, name='admin_engineer'),
    path('tax_payment_list/', views.tax_payments_list ,name='tax_payment_list'),
    path('admin_task/',views.admin_task ,name='admin_task'),
    path('notice/',views.notice ,name='notice'),
    path('admineditprofile/',views.admineditprofile , name='admineditprofile'),
    path('approve_engineer/<int:engineer_id>/', views.approve_engineer, name='approve_engineer'),
    path('reject_engineer/<int:engineer_id>/', views.reject_engineer, name='reject_engineer'),
    path("add-clerk/", views.add_clerk, name="add_clerk"),
    path("delete-clerks/", views.delete_clerks, name="delete_clerks"),
    path('document_approval/',views.document_approval,name = 'document_approval'),
    path('approve-document/<int:doc_id>/', views.approve_clerk_document, name='approve_clerk_document'),
    path('reject-document/<int:doc_id>/', views.reject_clerk_document, name='reject_clerk_document'),
    # path("leave-requests/", views.admin_leave_requests, name="admin_leave_requests"),
    # path("approve-leave/<int:leave_id>/", views.approve_leave, name="approve_leave"),
    # path("reject-leave/<int:leave_id>/", views.reject_leave, name="reject_leave"),
    path('leave-action/', views.leave_action, name='leave_action'),
    path('resolved/<int:complaint_id>', views.resolve_complaint, name='resolve_complaint'),

]

