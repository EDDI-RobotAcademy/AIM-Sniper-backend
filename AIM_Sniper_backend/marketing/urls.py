from django.urls import path, include
from rest_framework.routers import DefaultRouter

from marketing.controller.views import MarketingView

router = DefaultRouter()
router.register(r'marketing', MarketingView,basename='marketing')

urlpatterns = [
    path('', include(router.urls)),
    path('make-count', MarketingView.as_view({'post': 'clickCount'}), name='click_count')
]