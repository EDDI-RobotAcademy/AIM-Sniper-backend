from django.urls import path, include
from rest_framework.routers import DefaultRouter

from company_report.controller.views import CompanyReportView

router = DefaultRouter()
router.register(r'company_report', CompanyReportView)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', CompanyReportView.as_view({'get': 'list'}), name='company_report-list'),
    path('register', CompanyReportView.as_view({'post': 'register'}), name='company_report-register'),
    path('read/<int:pk>', CompanyReportView.as_view({'get': 'readCompanyReport'}), name='company_report-read'),
    path('delete/<int:pk>',CompanyReportView.as_view({'delete': 'deleteCompanyReport'}),name='company_report-delete'),
]