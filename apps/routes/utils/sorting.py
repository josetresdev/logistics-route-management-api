from rest_framework.filters import OrderingFilter

class StandardOrderingFilter(OrderingFilter):
    ordering_param = 'ordering'
