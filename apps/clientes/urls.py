from django.urls import path
from .views import ClienteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

urlpatterns = router.urls
