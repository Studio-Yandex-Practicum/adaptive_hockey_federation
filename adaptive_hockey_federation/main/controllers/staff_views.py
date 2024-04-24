from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import (
    StaffMemberForm,
    StaffTeamMemberEditForm,
    StaffTeamMemberForm,
)
from main.models import StaffMember, StaffTeamMember
from main.schemas.staff_schema import (
    STAFF_SEARCH_FIELDS,
    add_pisition_in_context,
    get_staff_fields,
    get_staff_table_data,
)


class StaffMemberListView(
    LoginRequiredMixin, PermissionRequiredMixin, ListView
):
    """Представление для работы со списком сотрудников."""

    model = StaffMember
    template_name = "main/staffs/staffs.html"
    permission_required = "main.list_view_staff"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр сотрудников."
    )
    context_object_name = "staffs"
    paginate_by = 10
    fields = (
        "id",
        "surname",
        "name",
        "patronymic",
        "phone",
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            search_column = self.request.GET.get("search_column")
            if not search_column or search_column.lower() in ["все", "all"]:
                or_lookup = (
                    Q(surname__icontains=search)
                    | Q(name__icontains=search)
                    | Q(patronymic__icontains=search)
                    | Q(phone__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = STAFF_SEARCH_FIELDS
                lookup = {f"{search_fields[search_column]}__icontains": search}
                queryset = queryset.filter(**lookup)

        return queryset.order_by("surname", "name", "patronymic")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        table_head = {}
        for field in self.fields:
            if field != "id":
                table_head[field] = self.model._meta.get_field(
                    field
                ).verbose_name
        context["table_head"] = table_head
        context["table_data"] = get_staff_table_data(context)
        return context


class StaffMemberIdView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    model = StaffMember
    template_name = "main/staffs/staff_id.html"
    context_object_name = "staff"
    fields = (
        "id",
        "surname",
        "name",
        "patronymic",
        "phone",
    )
    permission_required = "main.view_staffmember"
    permission_denied_message = (
        "У Вас нет разрешения на просмотр данных сотрудника."
    )

    def get_object(self, queryset=None):
        return get_object_or_404(StaffMember, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = context["staff"]
        queryset = StaffTeamMember.objects.filter(
            staff_member=self.kwargs["pk"]
        )
        if queryset.exists():
            queryset_coach = queryset.filter(staff_position="тренер")
            queryset_pusher = queryset.difference(queryset_coach)
            (context["coach"],
                context["team_fields_coach"]) = add_pisition_in_context(
                queryset_coach)
            (context["pusher"],
                context["team_fields_pusher"]) = add_pisition_in_context(
                queryset_pusher)
        context["staff_fields"] = get_staff_fields(staff)
        return context


class StaffMemberIdCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """Представление создания сотрудника."""

    model = StaffMember
    form_class = StaffMemberForm
    template_name = "main/staffs/staff_id_create_edit.html"
    success_url = reverse_lazy("main:staffs")
    permission_required = "main.add_staffmember"
    permission_denied_message = "У Вас нет разрешения на создание сотрудника."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Создание профиля нового сотрудника"
        return context

    def get_success_url(self):
        return reverse("main:staffs")


class StaffMemberIdEditView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """Представление редактирования сотрудника."""

    model = StaffMember
    form_class = StaffMemberForm
    template_name = "main/staffs/staff_id_create_edit.html"
    permission_required = "main.change_staffmember"
    permission_denied_message = (
        "У Вас нет разрешения на редактирование сотрудника."
    )

    def get_success_url(self):
        return reverse(
            "main:staff_id",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def get_object(self, queryset=None):
        return get_object_or_404(StaffMember, id=self.kwargs["pk"])


class StaffMemberIdDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    """Представление для удаления сотрудника."""

    model = StaffMember
    object = StaffMember
    success_url = reverse_lazy("main:staffs")
    permission_required = "main.delete_staffmember"
    permission_denied_message = "У Вас нет разрешения на удаление сотрудника."

    def get_object(self, queryset=None):
        return get_object_or_404(StaffMember, id=self.kwargs["pk"])


class StaffMemberIdTeamCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """Представление назначения сотрудника в команду"""

    model = StaffTeamMember
    form_class = StaffTeamMemberForm
    template_name = "main/staffs/staff_id_team_edit_create.html"
    permission_required = "main.change_staffteammember"
    permission_denied_message = "У Вас нет разрешения на"
    " редактирование сотрудника."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs["position"] == 'coach':
            context["page_title"] = (
                "Добавление сотрудника в команду тренером"
            )
        else:
            context["page_title"] = (
                "Добавление сотрудника в команду пушер-тьютором"
            )
        context["help_text_role"] = "Команды сотрудника"
        return context

    def get_success_url(self):
        return reverse(
            "main:staff_id",
            kwargs={
                "pk": self.get_object().pk,
            },
        )

    def get_object(self, queryset=None):
        return get_object_or_404(StaffMember, id=self.kwargs["pk"])

    def form_valid(self, form):
        positions = {
            'coach': 'тренер',
            'pusher': 'пушер-тьютор'
        }
        position = positions[self.kwargs["position"]]
        if form.cleaned_data.get('staff_posistion') is None:
            form.instance.staff_member = self.get_object()
            form.instance.staff_position = position
        return super(StaffMemberIdTeamCreateView, self).form_valid(form)


class StaffMemberIDTeamEditView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """Представление редактирования сотрудника находящегося в команде"""

    model = StaffTeamMember
    form_class = StaffTeamMemberEditForm
    template_name = "main/staffs/staff_id_team_edit_create.html"
    permission_required = "main.change_staffteammember"
    permission_denied_message = (
        "У Вас нет разрешения на редактирование сотрудника."
    )

    def get_success_url(self):
        return reverse(
            "main:staff_id",
            kwargs={
                "pk": self.object.staff_member.pk,
            },
        )

    def get_object(self, queryset=None):
        return get_object_or_404(StaffTeamMember, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = (
            f"Редактирование данных {self.get_object().staff_position}а"
            " команды")
        context["on_team"] = True
        context["help_text_role"] = "Команды сотрудника"
        return context


class StaffMemberIdTeamDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    """Представление для удаления сотрудника из команды"""

    model = StaffTeamMember
    object = StaffTeamMember
    permission_required = "main.change_staffteammember"
    permission_denied_message = "У Вас нет разрешения на удаление сотрудника."

    def get_object(self, queryset=None):
        return get_object_or_404(
            StaffTeamMember, id=self.kwargs["pk"])

    def get_success_url(self):
        return reverse(
            "main:staff_id",
            kwargs={
                "pk": self.get_object().staff_member.pk,
            },
        )
