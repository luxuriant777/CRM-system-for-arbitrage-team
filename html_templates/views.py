from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from html_templates.forms import LeadSearchForm, CustomUserSearchForm
from api_users.models import CustomUser
from api_leads.models import Lead
from .forms import CustomUserCreationForm, CustomUserUpdateForm


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
        context["user"] = self.get_object()
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
    paginate_by = 10
    search_form_class = LeadSearchForm

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)

        if form.is_valid():
            return Lead.objects.filter(
                Q(name__icontains=form.cleaned_data["search"])
            )


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lead
    template_name = "crm/lead_detail.html"


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
    return redirect('html_templates:lead-detail', pk=pk)
