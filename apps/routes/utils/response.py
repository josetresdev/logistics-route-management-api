"""
Standardized API response types and helper for Logistics Route Management API
Inspired by TranscriptlyAI (TypeScript version)
"""
from typing import Any, Dict, Optional, TypeVar, Generic, List, Union
from datetime import datetime

T = TypeVar("T")

class PaginationMeta:
    def __init__(self, current_page: int, per_page: int, total_items: int, total_pages: int):
        self.current_page = current_page
        self.per_page = per_page
        self.total_items = total_items
        self.total_pages = total_pages

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_page": self.current_page,
            "per_page": self.per_page,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
        }

class SortMeta:
    def __init__(self, sort_by: str, sort_order: str):
        self.sort_by = sort_by
        self.sort_order = sort_order

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
        }

class ErrorMeta:
    def __init__(self, timestamp: Optional[str] = None, version: str = "v1"):
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "version": self.version,
        }

class ErrorResponse:
    def __init__(self, message: str, code: str, details: Any = None, meta: Optional[ErrorMeta] = None):
        self.message = message
        self.code = code
        self.details = details
        self.meta = meta or ErrorMeta()

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "message": self.message,
            "code": self.code,
        }
        if self.details is not None:
            data["details"] = self.details
        if self.meta:
            data["meta"] = self.meta.to_dict()
        return data

class ApiResponse(Generic[T]):
    def __init__(
        self,
        success: bool,
        message: Optional[str] = None,
        data: Optional[T] = None,
        error: Optional[ErrorResponse] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        self.success = success
        self.message = message
        self.data = data
        self.error = error
        self.meta = meta

    def to_dict(self) -> Dict[str, Any]:
        result = {"success": self.success}
        if self.message:
            result["message"] = self.message
        if self.data is not None:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error.to_dict()
        if self.meta:
            result["meta"] = self.meta
        return result

# Helper for standardized responses
class ResponseHelper:
    @staticmethod
    def build_meta(
        pagination: Optional[PaginationMeta] = None,
        sort: Optional[SortMeta] = None,
    ) -> Dict[str, Any]:
        meta = {
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v1",
        }
        if pagination:
            meta["pagination"] = pagination.to_dict()
        if sort:
            meta["sort"] = sort.to_dict()
        return meta

    @staticmethod
    def ok(
        data: Any,
        message: str = "Request successful",
        pagination: Optional[PaginationMeta] = None,
        sort: Optional[SortMeta] = None,
    ) -> Dict[str, Any]:
        response = ApiResponse(
            success=True,
            message=message,
            data=ResponseHelper.normalize(data),
            meta=ResponseHelper.build_meta(pagination, sort),
        )
        return response.to_dict()

    @staticmethod
    def created(
        data: Any,
        message: str = "Resource created successfully",
    ) -> Dict[str, Any]:
        response = ApiResponse(
            success=True,
            message=message,
            data=ResponseHelper.normalize(data),
            meta=ResponseHelper.build_meta(),
        )
        return response.to_dict()

    @staticmethod
    def error(
        message: str,
        code: str = "APPLICATION_ERROR",
        status_code: int = 500,
        details: Any = None,
        meta_inside_error: Optional[ErrorMeta] = None,
    ) -> Dict[str, Any]:
        error_response = ErrorResponse(
            message=message,
            code=code,
            details=details,
            meta=meta_inside_error or ErrorMeta(),
        )
        response = ApiResponse(
            success=False,
            error=error_response,
        )
        return response.to_dict()

    @staticmethod
    def normalize(value: Any) -> Any:
        serialized = ResponseHelper.serialize_dates(value)
        return ResponseHelper.to_snake_case(serialized)

    @staticmethod
    def serialize_dates(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, list):
            return [ResponseHelper.serialize_dates(v) for v in value]
        if isinstance(value, dict):
            return {k: ResponseHelper.serialize_dates(v) for k, v in value.items()}
        return value

    @staticmethod
    def to_snake_case(value: Any) -> Any:
        import re
        if isinstance(value, list):
            return [ResponseHelper.to_snake_case(v) for v in value]
        if isinstance(value, dict):
            def snake(s):
                return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
            return {snake(k): ResponseHelper.to_snake_case(v) for k, v in value.items()}
        return value

    @staticmethod
    def from_exception(err: Exception) -> Dict[str, Any]:
        # You can customize this for your own exception types
        if hasattr(err, "status_code") and hasattr(err, "message"):
            return ResponseHelper.error(
                message=getattr(err, "message", "Application error"),
                code=getattr(err, "error_code", "APPLICATION_ERROR"),
                status_code=getattr(err, "status_code", 500),
            )
        else:
            return ResponseHelper.error(
                message="Internal server error",
                code="INTERNAL_ERROR",
                status_code=500,
            )

# Project repository URL
URL_REPO = "https://github.com/josetresdev/logistics-route-management-api"
from rest_framework.response import Response
from rest_framework import status


def standard_response(data=None, errors=None, status_code=status.HTTP_200_OK, pagination=None):
    resp = {
        "data": data,
        "errors": errors,
        "status": status_code,
    }
    if pagination:
        resp["pagination"] = pagination
    return Response(resp, status=status_code)


def paginated_response(queryset, serializer_class, request, view, errors=None):
    page = view.paginate_queryset(queryset)
    if page is not None:
        data = serializer_class(page, many=True).data
        pagination = {
            "count": view.paginator.page.paginator.count,
            "page": view.paginator.page.number,
            "page_size": view.paginator.page.paginator.per_page,
            "num_pages": view.paginator.page.paginator.num_pages,
        }
        return standard_response(data=data, errors=errors, status_code=status.HTTP_200_OK, pagination=pagination)
    data = serializer_class(queryset, many=True).data
    return standard_response(data=data, errors=errors, status_code=status.HTTP_200_OK)
