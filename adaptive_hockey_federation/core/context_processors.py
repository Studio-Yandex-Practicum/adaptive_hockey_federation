from main.schemas.main_schema import no_search_pages, show_return_button


def search_form_context(request):
    """Отвечает за правильное отображение поиска на страницах.
    Если нужно где-то убрать поле поиска, нужно внести изменения в список
    main/schemas/main_schema.py"""
    return {"no_search_pages": no_search_pages}


def return_button_context(request):
    return {"show_return_button": show_return_button}
