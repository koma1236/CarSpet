# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarDetailViewSet, CommentListView

router = DefaultRouter()
router.register(r'cars', CarDetailViewSet, basename='cars')

urlpatterns = [
    path('', include(router.urls)),
    path('cars/<int:car_id>/comments/', CommentListView.as_view(), name='car-comments'),
]
