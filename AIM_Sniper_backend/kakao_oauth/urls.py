from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kakao_oauth.controller.views import OauthView

router = DefaultRouter()
router.register(r'kakao_oauth', OauthView, basename='kakao_oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('kakao', OauthView.as_view({'get': 'kakaoOauthURI'}), name='get-kakao-oauth-uri'),
