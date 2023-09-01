from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponse, redirect, render

from .forms import ProjectForm, RegistrationForm
from .models import Project

from django.contrib import messages


# # Create your views here.


@login_required(login_url="/login")
def home(request):
    projects = Project.objects.all()
    if request.method == "POST":
        project_id = request.POST.get("project-id")
        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == request.user:
            project.delete()
            return redirect("/")
        else:
            amount_donated = request.POST.get("donation_amount")
            project.amount_donated += int(amount_donated)
            project.save()
            return redirect("/")

    return render(request, "home.html", {"projects": projects})


@login_required(login_url="/login")
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("/")
    else:
        form = ProjectForm()

    return render(request, "create.html", {"form": form})


@login_required(login_url="/login")
def edit_project(request, project_id):
    project = Project.objects.filter(id=project_id, owner=request.user).first()

    if not project:
        return HttpResponseForbidden("You do not have permission to edit this project.")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = ProjectForm(instance=project)

    return render(request, "edit.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegistrationForm()
    return render(request, "registration/sign-up.html", {"form": form})
