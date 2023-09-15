from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .forms import TodoForm, CustomUserCreationForm
from .models import Todo


@login_required
def index(request):
    todo = Todo.objects.filter(user=request.user)  # Filter todos by the current user
    form = TodoForm()
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            # Create a new Todo instance and set the user
            todo_item = form.save(commit=False)
            todo_item.user = request.user  # Assign the currently logged-in user
            todo_item.save()
            return redirect("index")

    context = {"todo": todo, "form": form}
    return render(request, "todo_list/index.html", context)


@login_required
def update(request, pk):
    todo = Todo.objects.get(id=pk)
    form = TodoForm(instance=todo)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("index")
    context = {"form": form}
    return render(request, "todo_list/edit.html", context)


@login_required
def delete(request, pk):
    todo = Todo.objects.get(id=pk)
    if request.method == "POST":
        todo.delete()
        return redirect("index")
    return render(request, "todo_list/delete.html", {"obj": todo})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("register")
    return render(request, "todo_list/delete_acc.html")
