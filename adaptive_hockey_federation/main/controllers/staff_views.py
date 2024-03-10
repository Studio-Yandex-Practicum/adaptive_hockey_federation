from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from core.utils import generate_file_name
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import StaffMemberForm, StaffTeamMemberForm
from main.models import StaffMember, StaffTeamMember


class StaffMemberListView(ListView):
    """Представление для работы со списком сотрудников команд."""
    model = StaffMember
    template_name = "main/staffs/staffs.html"
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
        table_head = {}
        for field in self.fields:
            if field != "id":
                table_head[field] = (
                    self.model._meta.get_field(field).verbose_name
                )
        context["table_head"] = table_head

        table_data = [
            {
                "surname": staff.surname,
                "name": staff.name,
                "patronymic": staff.patronymic,
                "phone": staff.phone,
                "url": reverse("main:staff_id", args=[staff.id]),
                "id": staff.pk,
            }
            for staff in context["staffs"]
        ]

        context["table_data"] = table_data
        return context


class StaffMemberIdView(PermissionRequiredMixin, DetailView):
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
    permission_required = 'main.view_staff'
    permission_denied_message = (
        "У Вас нет разрешения на просмотр данных персонала комаив.")

    def get_object(self, queryset=None):
        return get_object_or_404(StaffMember, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = context["staff"]

        staff_fields = [
            ("Фамилия", staff.surname),
            ("Имя", staff.name),
            ("Отчество", staff.patronymic),
            ("Номер телефона", staff.phone),
        ]

        queryset = StaffTeamMember.objects.filter(
            staff_member=self.kwargs["pk"]
        )
        team_fields = []
        for staff_team in queryset:
            team_fields.append(
                ("Команда",
                 ", ".join([team.name for team in staff_team.team.all()]))
            )
            team_fields.append(
                ("Статус сотрудника", staff_team.staff_position),
            )
            team_fields.append(
                ("Квалификация", staff_team.qualification),
            )
            team_fields.append(
                ("Описание", staff_team.notes),
            )
        context["staff_fields"] = staff_fields
        context["team_fields"] = team_fields
        return context


class StaffMemberIdCreateView(PermissionRequiredMixin, CreateView):
    """Представление создания сотрудника команды."""
    model = StaffMember
    form_class = StaffMemberForm
    template_name = "main/staffs/staff_id_create.html"
    success_url = reverse_lazy("main:staffs")
    permission_required = "main.add_staff"
    permission_denied_message = (
        "У Вас нет разрешения на создание карточки сотрудника команды.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        staff = form.save()
        team = form.cleaned_data['team']
        staff_position = form.cleaned_data['staff_position']
        qualification = form.cleaned_data['qualification']
        notes = form.cleaned_data['notes']
        try:
            staff_team = StaffTeamMember.objects.get(staff_member=staff)
            staff_team.staff_member = staff
            staff_team.staff_position = staff_position
            staff_team.qualification = qualification
            staff_team.notes = notes
        except StaffTeamMember.DoesNotExist:
            staff_team = StaffTeamMember.objects.create(
                staff_member=staff,
                staff_position=staff_position,
                qualification=qualification,
                notes=notes
            )
        staff_team.team.set([t.id for t in team])
        staff_team.save()
        return super().form_valid(form)


class StaffMemberIdEditView(PermissionRequiredMixin, UpdateView):
    """Представление редактирования сотрудника команды."""
    model = StaffMember
    form_class = StaffMemberForm
    template_name = "main/staffs/staff_id_edit.html"
    success_url = reverse_lazy("main:staffs")
    permission_required = "main.change_staff"
    permission_denied_message = (
        "У Вас нет разрешения на редактирование карточки сотрудника команды.")

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.get_object()
        staff_team = StaffTeamMember.objects.get(staff_member=staff)
        
        print(f'>>> context >>>> {context}')
        return context

    def form_valid(self, form):
        staff = form.save()
        team = form.cleaned_data['team']
        staff_position = form.cleaned_data['staff_position']
        qualification = form.cleaned_data['qualification']
        notes = form.cleaned_data['notes']
        try:
            staff_team = StaffTeamMember.objects.get(staff_member=staff)
            staff_team.staff_member = staff
            staff_team.staff_position = staff_position
            staff_team.qualification = qualification
            staff_team.notes = notes
        except StaffTeamMember.DoesNotExist:
            staff_team = StaffTeamMember.objects.create(
                staff_member=staff,
                staff_position=staff_position,
                qualification=qualification,
                notes=notes
            )
        print(f'>>> staff_team >>>> {staff_team}')
        staff_team.team.set([t.id for t in team])
        staff_team.save()
        return super().form_valid(form)


class StaffMemberIdDeleteView(PermissionRequiredMixin, DeleteView):
    """Представление для удаления сотрудника команды."""
    model = StaffMember
    object = StaffMember
    success_url = reverse_lazy("main:staffs")
    permission_required = "main.delete_staff"
    permission_denied_message = (
        'У Вас нет разрешения на удаление персонала команд.')

    def get_object(self, queryset=None):
        return get_object_or_404(StaffMember, id=self.kwargs["pk"])


class StaffTeamMemberCreateView(PermissionRequiredMixin, CreateView):
    """Представление для создания нового сотрудника команды."""
    model = StaffTeamMember
    form_class = StaffTeamMemberForm
    template_name = "main/staffs/staff_member_create.html"
    permission_required = "main.add_staff"
    permission_denied_message = (
        "У Вас нет разрешения на создание карточки сотрудника команды.")
    team_id = None

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.team_id = request.GET.get('team', None)
        if self.team_id is not None:
            self.initial = {'team': self.team_id}
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_id'] = self.team_id
        return context

    def get_success_url(self):
        if 'None' in self.team_id or self.team_id is None:
            return reverse('main:players')
        else:
            return reverse('main:teams_id', kwargs={'team_id': self.team_id})

    def post(self, request, *args, **kwargs):
        self.team_id = request.POST.get('team_id')
        return super().post(request, *args, **kwargs)
