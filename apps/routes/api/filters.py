import django_filters
from apps.routes.domain.models import Route


class RouteFilterSet(django_filters.FilterSet):
    """
    FilterSet personalizado para rutas con búsqueda avanzada.
    """
    
    # Filtros básicos
    status = django_filters.CharFilter(
        field_name="status__code",
        lookup_expr="iexact",
        label="Status Code"
    )
    
    priority = django_filters.NumberFilter(
        field_name="priority__level",
        lookup_expr="exact",
        label="Priority Level"
    )
    
    # Filtros de ubicación
    origin = django_filters.NumberFilter(
        field_name="origin_id",
        lookup_expr="exact",
        label="Origin Location ID"
    )
    
    destination = django_filters.NumberFilter(
        field_name="destination_id",
        lookup_expr="exact",
        label="Destination Location ID"
    )
    
    # Filtros de fecha
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Created After"
    )
    
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Created Before"
    )
    
    # Filtro de distancia
    min_distance = django_filters.NumberFilter(
        field_name="distance_km",
        lookup_expr="gte",
        label="Minimum Distance (km)"
    )
    
    max_distance = django_filters.NumberFilter(
        field_name="distance_km",
        lookup_expr="lte",
        label="Maximum Distance (km)"
    )
    
    # Filtro por lote
    batch = django_filters.NumberFilter(
        field_name="batch_id",
        lookup_expr="exact",
        label="Import Batch ID"
    )

    class Meta:
        model = Route
        fields = [
            "status",
            "priority",
            "origin",
            "destination",
            "created_after",
            "created_before",
            "min_distance",
            "max_distance",
            "batch",
        ]
