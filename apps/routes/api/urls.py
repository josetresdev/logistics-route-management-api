
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from apps.routes.api.views import (
    RouteViewSet,
    RouteStatusViewSet,
    PriorityCatalogViewSet,
    GeographicLocationViewSet,
    ExecutionLogViewSet,
    ImportBatchViewSet,
)

# Crear router y registrar viewsets
router = DefaultRouter()
router.register(r"routes", RouteViewSet, basename="route")
router.register(r"route-statuses", RouteStatusViewSet, basename="route-status")
router.register(r"priorities", PriorityCatalogViewSet, basename="priority")
router.register(r"locations", GeographicLocationViewSet, basename="location")
router.register(r"execution-logs", ExecutionLogViewSet, basename="execution-log")
router.register(r"import-batches", ImportBatchViewSet, basename="import-batch")

urlpatterns = [
    path("", include(router.urls)),
    path("token-auth/", obtain_auth_token),
]
