from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Vuln, Remedy
from django.db.models import Q
from .forms import RemedyForm
from functools import reduce
import operator


def dashboard(request):
    template = "vulns/dashboard.html"
    context = dict(title="Dashboard")
    return render(request, template, context)


class VulnListView(ListView):
    model = Vuln
    context_object_name = "vulns"
    ordering = ["-date_posted"]
    paginate_by = 5


class ReversedVulnListView(ListView):
    model = Vuln
    context_object_name = "vulns"
    ordering = ["date_posted"]
    paginate_by = 5


class RankedVulnListView(ListView):
    model = Vuln
    context_object_name = "vulns"
    ordering = ["-risk_score"]
    paginate_by = 5


class RemedyListView(ListView):
    model = Remedy
    context_object_name = "rems"
    ordering = ["-date_posted"]
    paginate_by = 5


class VulnDetailView(DetailView):
    model = Vuln


class VulnCreateView(LoginRequiredMixin, CreateView):
    model = Vuln
    fields = ["cve", "title", "risk_score", "summary"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class VulnUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vuln
    fields = ["cve", "title", "risk_score", "summary"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        vuln = self.get_object()
        if self.request.user == vuln.author:
            return True
        else:
            return False


class VulnDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vuln
    success_url = "/vuln/"

    def test_func(self):
        vuln = self.get_object()
        if self.request.user == vuln.author:
            return True
        else:
            return False


@login_required
def add_remedy(request, pk):
    vuln = get_object_or_404(Vuln, pk=pk)
    if request.method == "POST":
        r_form = RemedyForm(request.POST)
        if r_form.is_valid():
            remedy = r_form.save(commit=False)
            remedy.vulnerability = vuln
            remedy.author = request.user
            remedy.save()
            return redirect("vuln-detail", vuln.id)
    else:
        r_form = RemedyForm()
    context = dict(form=r_form)
    template = 'vulns/add_remedy.html'
    return render(request, template, context)


@login_required
def export_csv(request, pk):
    vuln = get_object_or_404(Vuln, pk=pk)
    csv_lines = ["cve,author,remediation,status,patches"]
    for rem in vuln.rems.all():
        csv_lines.append(
            ",".join((
                repr(vuln.cve),
                repr(rem.author.username),
                repr(rem.remediation),
                repr(rem.status),
                repr(rem.patches)
            ))
        )
    template = "vulns/export_csv.html"
    context = dict(title="Export", vuln_csv=csv_lines)
    return render(request, template, context)


class VulnSearchListView(VulnListView):
    paginate_by = 5

    def get_queryset(self):
        result = super(VulnSearchListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(cve__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(risk_score__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(summary__icontains=q) for q in query_list))
            )
        return result


class RemedySearchListView(RemedyListView):
    paginate_by = 5

    def get_queryset(self):
        result = super(RemedySearchListView, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(remediation__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(status__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(patches__icontains=q) for q in query_list))
            )
        return result
