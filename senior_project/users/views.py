from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User
from django.views.generic import ListView
from vulns.models import Vuln, Remedy
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form_obj = UserRegisterForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            username = form_obj.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form_obj = UserRegisterForm()
    context = dict(title="Register", form=form_obj)
    return render(request, "users/register.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
    template = "users/profile.html"
    context = dict(title="Profile", form=u_form)
    return render(request, "users/profile.html", context)


class UserVulnListView(ListView):
    model = Vuln
    context_object_name = "vulns"
    template_name = "users/user_vulns.html"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Vuln.objects.filter(author=user).order_by("-date_posted")


class UserRemedyListView(ListView):
    model = Remedy
    context_object_name = "rems"
    template_name = "users/user_rems.html"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Remedy.objects.filter(author=user).order_by("-date_posted")
