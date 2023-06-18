from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django_tables2 import RequestConfig, SingleTableView

from analytics.graphs import create_graphs
from api_teams.models import Team
from .forms import TeamSearchForm, ProspectSearchForm, CustomUserSearchForm, CustomUserCreationForm, CustomUserUpdateForm
from api_users.models import CustomUser, Position
from api_prospects.models import Prospect
from .tables import TeamTableView, ProspectTableView, ProspectTableForCustomUser, CustomUserTable


@login_required
def index(request):
    return render(request, "crm/index.html")

class UserMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        prospects = Prospect.objects.filter(user_id=user.id).order_by("-created_at")
        context["user"] = user
        context["prospects"] = prospects
        return context

class SearchFormMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get("search", "")
        context["search_form"] = self.search_form_class(initial={"search": search})

        return context

class TeamListView(LoginRequiredMixin, SearchFormMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"
    template_name = "crm/team_list.html"
    search_form_class = TeamSearchForm

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)
        if form.is_valid() and form.cleaned_data["search"]:
            search_term = form.cleaned_data["search"]
            return Team.objects.filter(
                Q(name__icontains=search_term) |
                Q(team_lead__first_name__icontains=search_term) |
                Q(team_lead__last_name__icontains=search_term)
            )
        return Team.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = self.get_queryset()
        table = TeamTableView(teams)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["team_table"] = table
        return context

class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "crm/team_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context["team_members"] = team.members.all()
        context["team_lead"] = team.team_lead
        context["member_table"] = CustomUserTable(team.members.all())
        return context

class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("html_templates:team-list")
    template_name = "crm/team_form.html"

class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    template_name = "crm/team_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "html_templates:team-detail", kwargs={"pk": self.object.pk}
        )

class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("html_templates:team-list")
    template_name = "crm/team_confirm_delete.html"

class ProspectListView(LoginRequiredMixin, SearchFormMixin, generic.ListView):
    model = Prospect
    context_object_name = "prospect_list"
    template_name = "crm/prospect_list.html"
    search_form_class = ProspectSearchForm

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            return Prospect.objects.filter(
                Q(id__icontains=form.cleaned_data["search"]) |
                Q(ip_address__icontains=form.cleaned_data["search"]) |
                Q(user_agent__icontains=form.cleaned_data["search"]) |
                Q(referral_source__icontains=form.cleaned_data["search"])
            ).order_by("-created_at")

        return Prospect.objects.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prospects = self.get_queryset()
        table = ProspectTableView(prospects)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["prospect_table"] = table
        return context

class ProspectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Prospect
    template_name = "crm/prospect_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prospect = self.get_object()
        try:
            user = CustomUser.objects.get(id=prospect.user_id)
        except CustomUser.DoesNotExist:
            user = None
        context["user"] = user
        if user:
            context["user_table"] = CustomUserTable([user])
        return context

class ProspectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Prospect
    fields = "__all__"
    success_url = reverse_lazy("html_templates:prospect-list")
    template_name = "crm/prospect_form.html"


class ProspectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Prospect
    fields = "__all__"
    template_name = "crm/prospect_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "html_templates:prospect-detail", kwargs={"pk": self.object.pk}
        )

class ProspectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Prospect
    success_url = reverse_lazy("html_templates:prospect-list")
    template_name = "crm/prospect_confirm_delete.html"

class CustomUserListView(LoginRequiredMixin, SearchFormMixin, SingleTableView):
    model = CustomUser
    context_object_name = "user_list"
    table_class = CustomUserTable
    template_name = "crm/user_list.html"
    search_form_class = CustomUserSearchForm

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            return CustomUser.objects.filter(
                Q(first_name__icontains=form.cleaned_data["search"]) |
                Q(last_name__icontains=form.cleaned_data["search"]) |
                Q(username__icontains=form.cleaned_data["search"])
            )
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = self.get_queryset()
        table = CustomUserTable(users)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["user_table"] = table
        return context

class CustomUserDetailView(LoginRequiredMixin, UserMixin, generic.DetailView):
    model = CustomUser
    template_name = "crm/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        prospects = Prospect.objects.filter(user_id=user.id).order_by("-created_at")
        table = ProspectTableForCustomUser(prospects)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["prospect_table"] = table
        return context

class CustomUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("html_templates:user-list")
    template_name = "crm/user_form.html"

class CustomUserUpdateView(LoginRequiredMixin, UserMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy("html_templates:user-list")
    template_name = "crm/user_form.html"

class CustomUserDeleteView(LoginRequiredMixin, UserMixin, generic.DeleteView):
    model = CustomUser
    success_url = reverse_lazy("html_templates:user-list")
    template_name = "crm/user_confirm_delete.html"
