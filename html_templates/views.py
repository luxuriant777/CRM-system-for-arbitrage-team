from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django_tables2 import RequestConfig, SingleTableView, LazyPaginator

from html_templates.forms import LeadSearchForm, CustomUserSearchForm
from api_users.models import CustomUser
from api_leads.models import Lead
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .tables import LeadTableByUser
from .tables import LeadTableAllUsers


def index(request):
    num_users = CustomUser.objects.count()
    num_leads = Lead.objects.count()

    context = {
        "num_users": num_users,
        "num_leads": num_leads,
    }

    return render(request, "crm/index.html", context=context)


class UserMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        leads = Lead.objects.filter(user_id=user.id).order_by("-created_at")
        context["user"] = user
        context["leads"] = leads
        return context


class SearchFormMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get("search", "")
        context["search_form"] = self.search_form_class(initial={"search": search})

        return context


class LeadListView(LoginRequiredMixin, SearchFormMixin, generic.ListView):
    model = Lead
    context_object_name = "lead_list"
    template_name = "crm/lead_list.html"
    search_form_class = LeadSearchForm

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            return Lead.objects.filter(
                Q(id__icontains=form.cleaned_data["search"]) |
                Q(ip_address__icontains=form.cleaned_data["search"]) |
                Q(user_agent__icontains=form.cleaned_data["search"]) |
                Q(referral_source__icontains=form.cleaned_data["search"])
            ).order_by("-created_at")

        return Lead.objects.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        leads = self.get_queryset()
        table = LeadTableAllUsers(leads)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["table"] = table
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lead
    template_name = "crm/lead_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = context["lead"]
        context["user"] = get_object_or_404(CustomUser, id=lead.user_id)
        return context


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    model = Lead
    fields = "__all__"
    success_url = reverse_lazy("html_templates:lead-list")
    template_name = "crm/lead_form.html"


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lead
    fields = "__all__"
    template_name = "crm/lead_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "html_templates:lead-detail", kwargs={"pk": self.object.pk}
        )


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Lead
    success_url = reverse_lazy("html_templates:lead-list")
    template_name = "crm/lead_confirm_delete.html"


class CustomUserListView(LoginRequiredMixin, SearchFormMixin, generic.ListView):
    model = CustomUser
    paginate_by = 10
    template_name = "crm/user_list.html"
    context_object_name = "user_list"
    search_form_class = CustomUserSearchForm

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)

        if form.is_valid():
            return CustomUser.objects.filter(
                Q(first_name__icontains=form.cleaned_data["search"]) |
                Q(last_name__icontains=form.cleaned_data["search"]) |
                Q(username__icontains=form.cleaned_data["search"])
            )


class CustomUserDetailView(LoginRequiredMixin, UserMixin, generic.DetailView):
    model = CustomUser
    template_name = "crm/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        leads = Lead.objects.filter(user_id=user.id).order_by("-created_at")
        table = LeadTableByUser(leads)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context["lead_table"] = table
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


@login_required
def toggle_lead_assign(request, pk):
    user = request.user
    if Lead.objects.get(id=pk) in user.leads.all():
        user.leads.remove(pk)
    else:
        user.leads.add(pk)
    return redirect("html_templates:lead-detail", pk=pk)
