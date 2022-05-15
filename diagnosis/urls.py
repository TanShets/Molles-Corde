from django.urls import path
from . import views

urlpatterns = [
    path('', views.DiagnosisLanding, name = 'diagnosis-landing'),
    path('single-patient', views.DiagnosisSinglePatient, name = 'diagnosis-home'),
    path('multi-patient', views.DiagnosisMultiPatient, name = 'diagnosis-multipatient'),
    path('chd', views.DiagnosisCHD, name = 'diagnosis-chd'),
    path('cvd', views.DiagnosisCVD, name = 'diagnosis-cvd'),
    path('hyp', views.DiagnosisHyp, name = 'diagnosis-hyp'),
    path('arr', views.DiagnosisArrhymthmia, name = 'diagnosis-arr'),
    path('result', views.DownloadPage, name = 'diagnosis-download')
]
