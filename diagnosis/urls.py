from django.urls import path
from . import views

urlpatterns = [
    path('', views.DiagnosisHome, name = 'diagnosis-home'),
    path('chd', views.DiagnosisCHD, name = 'diagnosis-chd'),
    path('cvd', views.DiagnosisCVD, name = 'diagnosis-cvd'),
    path('hyp', views.DiagnosisHyp, name = 'diagnosis-hyp'),
    path('arr', views.DiagnosisArrhymthmia, name = 'diagnosis-arr'),
]
