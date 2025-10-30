from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import TodoItem
from .forms import UserRegistrationForm

@login_required
def home(request):
    if request.method == 'POST':
        todo_name = request.POST.get("new-todo")
        if todo_name:
            TodoItem.objects.create(name=todo_name, user=request.user)
        return redirect("home")

    todos = TodoItem.objects.filter(user=request.user).order_by("-created_on")
    paginator = Paginator(todos, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "crud.html", context)

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.delete()
    return redirect('home')

@login_required
def complete_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.is_completed = True
    todo.save()
    return redirect('home')

def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {"form": form}
    return render(request, "register.html", context)
