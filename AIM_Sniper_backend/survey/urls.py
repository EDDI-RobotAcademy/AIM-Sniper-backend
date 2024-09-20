from django.urls import path, include
from rest_framework.routers import DefaultRouter

from survey.controller.views import SurveyView

router = DefaultRouter()
router.register(r'survey', SurveyView, basename='survey')

urlpatterns = [
    path('', include(router.urls)),
    path('creat-form', SurveyView.as_view({'post':'createSurveyForm'}), name='survey-create-form'),
    path('register-title-description', SurveyView.as_view({'post':'registerTitleDescription'}), name='register-title-description'),
    path('register-question', SurveyView.as_view({'post':'registerQuestion'}), name='survey-question'),
    path('register-selection', SurveyView.as_view({'post':'registerSelection'}), name='survey-selection'),
    path('read-survey-form', SurveyView.as_view({'post': 'readSurveyForm'}), name='read-survey-form'),
]