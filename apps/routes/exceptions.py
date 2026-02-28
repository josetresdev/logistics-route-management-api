from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response


class RouteNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Route not found."
    default_code = "route_not_found"


class InvalidRouteData(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid route data provided."
    default_code = "invalid_route_data"


class ImportError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Error during import process."
    default_code = "import_error"


class ExecutionError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Error during route execution."
    default_code = "execution_error"


def custom_exception_handler(exc, context):
    """
    Custom exception handler for standardized API responses.
    
    Returns a standardized error response for all exceptions.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            "data": None,
            "errors": response.data,
            "status": response.status_code,
        }
    
    return response
