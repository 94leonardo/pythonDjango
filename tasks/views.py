from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here. ruta de las vistas


def home(request):

    return render(request, "home.html")


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        tasks = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=tasks)
        return render(request, "task_detail.html", {"task": tasks, "form": form})

    else:
        try:
            tasks = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=tasks)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": tasks, "form": form, "error": "error updating task"},
            )


@login_required
def complete_task(request, task_id):
    tasks = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        tasks.datecompleted = timezone.now()
        tasks.save()
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    tasks = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        tasks.delete()
        return redirect("tasks")


def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # registro user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )

                user.save()
                login(request, user)
                return redirect("tasks")

            except IntegrityError:

                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "User already exist"},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Password do not match"},
        )


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def create_task(request):

    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {
                    "form": TaskForm,
                    "error": "Please provide valida data",
                },
            )


@login_required
def signout(request):

    logout(request)
    return redirect("home")


def signin(request):

    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
                status=401,
            )
        else:
            login(request, user)
            return redirect("tasks")
