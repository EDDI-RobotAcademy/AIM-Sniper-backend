from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview.controller.views import InterviewView

router = DefaultRouter()
router.register(r'interview', InterviewView, basename='interview')
urlpatterns = [
    path('', include(router.urls)),
    path('insert-session', InterviewView.as_view({'post': 'insertSession'}), name='insert-session'),
    path('get-session', InterviewView.as_view({'post': 'getSession'}), name='get-session'),
]
