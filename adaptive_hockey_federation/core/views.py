from http import HTTPStatus

from django.shortcuts import render


def not_found(request, exception):
    """Представление ошибки 404."""
    return render(
        request=request,
        template_name="error-pages/404.html",
        context={"path": request.path},
        status=HTTPStatus.NOT_FOUND,
    )


def forbidden(request, exception):
    """Представление ошибки 403."""
    return render(
        request=request,
        template_name="error-pages/403.html",
        context={"path": request.path},
        status=HTTPStatus.FORBIDDEN,
    )


def internal_server_error(request):
    """Представление ошибки 500."""
    return render(
        request=request,
        template_name="error-pages/500.html",
        context={"path": request.path},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
