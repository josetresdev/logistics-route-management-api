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
