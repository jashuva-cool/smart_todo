from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    # Reminder Notification
    for task in tasks:
        if not task.completed and task.due_date <= timezone.now():
            messages.warning(request, f"Task '{task.title}' is pending!")

    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def add_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('dashboard')
    return render(request, 'task_form.html', {'form': form})

@login_required
def update_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'task_form.html', {'form': form})

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('dashboard')

@login_required
def toggle_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')