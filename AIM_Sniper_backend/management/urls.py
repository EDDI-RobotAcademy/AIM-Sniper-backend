from django.urls import path, include
from rest_framework.routers import DefaultRouter

from management.controller.views import ManagementView

router = DefaultRouter()
router.register(r'management', ManagementView, basename='management')

urlpatterns = [
    path('', include(router.urls)),
    path('userList', ManagementView.as_view({'get': 'userList'}), name='user-list'),
    path('grant-roleType',ManagementView.as_view({'post':'grantRoleType'}),name='account-grant-role-type'),
    path('revoke-roleType',ManagementView.as_view({'post':'revokeRoleType'}),name='account-revoke-role-type'),
]