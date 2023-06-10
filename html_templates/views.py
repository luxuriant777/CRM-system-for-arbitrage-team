from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from html_templates.forms import LeadSearchForm, CustomUserSearchForm
from user_management.models import CustomUser
from customer_management.models import Lead


def index(request):
    num_users = CustomUser.objects.count()
    num_leads = Lead.objects.count()

    context = {
        "num_users": num_users,
        "num_leads": num_leads,
    }

    return render(request, "crm/index.html", context=context)


class LeadListView(LoginRequiredMixin, generic.ListView):
    model = Lead
    context_object_name = "lead_list"
    template_name = "crm/lead_list.html"
    queryset = Lead.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)

        search = self.request.GET.get("search", "")
        is_completed = self.request.GET.get("is_completed", "")

        context["search_form"] = LeadSearchForm(
            initial={"search": search, "is_completed": is_completed}
        )

        return context

    def get_queryset(self):
        form = LeadSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["is_completed"]:
                return self.queryset.filter(
                    name__icontains=form.cleaned_data["search"],
                    is_completed=True,
                )
            return self.queryset.filter(
                name__icontains=form.cleaned_data["search"]
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


class CustomUserListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    queryset = CustomUser.objects.all()
    paginate_by = 5
    template_name = "crm/user_list.html"
    context_object_name = "user_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomUserListView, self).get_context_data(**kwargs)

        search = self.request.GET.get("search", "")

        context["search_form"] = CustomUserSearchForm(initial={"search": search})
        return context

    def get_queryset(self):
        form = CustomUserSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                Q(first_name__icontains=form.cleaned_data["search"])
                | Q(first_name__icontains=form.cleaned_data["search"])
                | Q(username__icontains=form.cleaned_data["search"])
            )


class CustomUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    queryset = CustomUser.objects.all()
    template_name = "crm/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context


class CustomUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = CustomUser
    fields = "__all__"
    success_url = reverse_lazy("html_templates:user-list")
    template_name = "crm/user_form.html"


class CustomUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    fields = "__all__"
    success_url = reverse_lazy("html_templates:user-list")
    template_name = "crm/user_form.html"


class CustomUserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CustomUser
    success_url = reverse_lazy("html_templates:user-list")
    template_name = "crm/user_confirm_delete.html"


@login_required
def toggle_lead_assign(request, pk):
    user = CustomUser.objects.get(id=request.user.id)
    if Lead.objects.get(id=pk) in user.leads.all():
        user.leads.remove(pk)
    else:
        user.leads.add(pk)
    return HttpResponseRedirect(
        reverse_lazy("html_templates:lead-detail", args=[pk])
    )
