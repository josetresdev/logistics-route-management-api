from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        resp = {
            "data": None,
            "errors": response.data,
            "status": response.status_code,
        }
        return Response(resp, status=response.status_code)
    # Fallback for unhandled errors
    return Response({
        "data": None,
        "errors": {"detail": "Internal server error."},
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
