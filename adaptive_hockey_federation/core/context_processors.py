from main.schemas.main_schema import no_search_pages


def search_form_context(request):
    return {"no_search_pages": no_search_pages}
