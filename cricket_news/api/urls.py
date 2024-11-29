from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.news import NewsViewSet
from .views.user import UserDetailView

router = DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]