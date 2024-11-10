from django.urls import path
from . import views

urlpatterns = [
    path('client/', views.client_report_view, name='client_report'),  # Para informes generales de clientes
    path('generate/', views.generate_report_view, name='generate_report'),  # Genera informe personalizado
    path('project/<int:project_id>/report/', views.project_report, name='project_report'),  # Informe de un proyecto específico
    path('client/report/<int:report_id>/', views.view_report_detail, name='view_report_detail'),  # Detalle de informe específico

]
