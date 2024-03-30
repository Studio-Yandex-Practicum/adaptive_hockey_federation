from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import StaffMemberForm, StaffTeamMemberForm
from main.models import StaffMember, StaffTeamMember
from main.schemas import staff_schema


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
                search_fields = {
                    "surname": "surname",
                    "name": "name",
                    "patronymic": "patronymic",
                    "phone": "phone",
                }
                lookup = {f"{search_fields[search_column]}__icontains": search}
                queryset = queryset.filter(**lookup)

        return queryset.order_by("surname", "name", "patronymic")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = staff_schema.staff_list_table(self, context)
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
        context = staff_schema.staff_id_list(self, context)
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
    team_id: int | None = None

    def form_valid(self, form):
        context = self.get_context_data()
        staff_form = context["staff_form"]
        with transaction.atomic():
            self.object = form.save()
            if staff_form.is_valid():
                staff_form.instance.staff_member = self.object
                staff_form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            form = StaffTeamMemberForm(self.request.POST)
        else:
            form = StaffTeamMemberForm(initial={"team": self.team_id})
        context["page_title"] = "Создание профиля нового сотрудника"
        context["staff_form"] = form
        context["team_id"] = self.team_id
        return context

    def get(self, request, *args, **kwargs):
        self.team_id = request.GET.get("team", None)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.team_id is None:
            return reverse("main:staffs")
        else:
            return reverse("main:teams_id", kwargs={"team_id": self.team_id})

    def post(self, request, *args, **kwargs):
        self.team_id = request.POST.get("team_id", None)
        return super().post(request, *args, **kwargs)


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

    def form_valid(self, form):
        context = self.get_context_data()
        staff_form = context["staff_form"]
        context["page_title"] = "Редактирование профиля сотрудника"
        with transaction.atomic():
            form.save()
            if staff_form.is_valid():
                staff_form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = StaffTeamMember.objects.get(staff_member=self.object)
        if self.request.POST:
            context["staff_form"] = StaffTeamMemberForm(
                self.request.POST, instance=staff
            )
        else:
            context["staff_form"] = StaffTeamMemberForm(instance=staff)
        return context


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
