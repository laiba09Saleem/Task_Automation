# tasks/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from django.contrib.auth.models import User

from .models import Task, TaskAssignment, Notifications
from .serializers import TaskSerializer, TaskAssignmentSerializer, NotificationSerializer
from .forms import TaskForm


# ------------------ USER AUTH ------------------ #

def signup_view(request):
    """Register new user"""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check username availability
        if User.objects.filter(username=username).exists():
            return render(request, "tasks/signup.html", {
                "error": "Username already taken!"
            })

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "tasks/signup.html")


def login_view(request):
    """Login existing user"""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            return render(request, "tasks/login.html", {
                "error": "User not registered! Please create an account first."
            })

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "tasks/login.html", {
                "error": "Incorrect password!"
            })

    return render(request, 'tasks/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------ DASHBOARD ------------------ #

@login_required
def dashboard(request):
    tasks = Task.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})


# ------------------ API ViewSets ------------------ #

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        assignee_id = request.data.get('assignee_id')

        if not assignee_id:
            return Response({'detail': 'assignee_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=assignee_id)
        except User.DoesNotExist:
            return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        assignment, created = TaskAssignment.objects.get_or_create(task=task, assignee=user)
        return Response(TaskAssignmentSerializer(assignment).data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notifications.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


# ------------------ TASK CRUD ------------------ #

@login_required
@require_http_methods(["GET", "POST"])
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()

            # Save assigned users
            assignees = form.cleaned_data.get('assignees')
            if assignees:
                for u in assignees:
                    TaskAssignment.objects.get_or_create(task=task, assignee=u)

            return redirect('task_list')

    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            # Remove old assignments
            TaskAssignment.objects.filter(task=task).delete()

            # Add new assignments
            assignees = form.cleaned_data.get("assignees")
            if assignees:
                for user in assignees:
                    TaskAssignment.objects.get_or_create(task=task, assignee=user)

            return redirect("task_list")

    else:
        form = TaskForm(instance=task)
        existing = task.assignments.values_list("assignee_id", flat=True)
        form.fields["assignees"].initial = existing

    return render(request, "tasks/task_form.html", {
        "form": form,
        "update": True,
    })


@login_required
@require_http_methods(["POST"])
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    task.delete()
    return redirect('task_list')


@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
