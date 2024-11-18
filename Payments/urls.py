from django.urls import path
from . import views

urlpatterns = [
    path('client/payments/', views.client_payment_history, name='client_payment_history'),
    path('freelancer/payments/', views.freelancer_payment_history, name='freelancer_payment_history'),
    path('freelancers_project_pay/<int:project_id>/', views.freelancers_project_pay, name='freelancers_project_pay'),
    path('project/<int:project_id>/freelancer/<int:freelancer_id>/punctual-pay/', views.freelancers_project_punctual_pay, name='freelancers_project_punctual_pay'),
    path('project/<int:project_id>/freelancer/<int:freelancer_id>/periodic-pay/', views.freelancers_project_periodic_pay, name='freelancers_project_periodic_pay'),
    path('pending-payments/', views.pending_payments, name='pending_payments'),
    path('completed-payments/', views.completed_payments, name='completed_payments'),
    path('pay/<int:payment_id>/', views.make_payment, name='make_payment'),
    path('project/<int:project_id>/freelancer/<int:freelancer_id>/choose-method/', views.choose_payment_method, name='choose_payment_method'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='payment_receipt'),
]
