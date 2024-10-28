from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview_result.controller.views import InterviewResultView

router = DefaultRouter()
router.register(r'interview_result', InterviewResultView, basename='interview_result')
urlpatterns = [
    path('', include(router.urls)),
    path('save-interview-result', InterviewResultView.as_view({'post': 'saveInterviewResult'}), name='save-interview-result'),
    path('get-interview-result', InterviewResultView.as_view({'post': 'getInterviewResult'}), name='get-interview-result'),
]
