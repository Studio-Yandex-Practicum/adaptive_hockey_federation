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
