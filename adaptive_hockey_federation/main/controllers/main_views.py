from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.views.generic.list import ListView
from main.models import Player
from main.schemas.main_schema import get_main_table_data


class MainView(
    LoginRequiredMixin,
    ListView,
):
    """Main_view. Поиск игроков по фамилии/имени."""

    model = Player
    template_name = "main/home/main.html"
    context_object_name = "main"
    fields = [
        "id",
        "surname",
        "name",
        "birthday",
        "gender",
        "number",
        "discipline_name",
        "discipline_level",
        "diagnosis",
    ]

    def get_queryset(self):
        query = self.request.GET.get("search")
        search_vector = SearchVector("surname", "name")
        queryset = None
        if query:
            queryset = Player.objects.annotate(search=search_vector).filter(
                search=query,
            )
            queryset = (
                queryset.select_related("diagnosis")
                .select_related("discipline_name")
                .order_by("surname")
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            table_head = {}
            for field in self.fields:
                if field != "id":
                    table_head[field] = Player._meta.get_field(
                        field,
                    ).verbose_name
            context["table_head"] = table_head
            context["table_data"] = get_main_table_data(context)
        return context
