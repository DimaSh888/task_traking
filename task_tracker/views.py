from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import TaskForm, TaskFlterForm
from .mixins import UserIsOwnerMixin
# Create your views here.


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFlterForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    context_object_name = 'task'
    form_class = TaskForm
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-list")


class TaskDeleteView(UserIsOwnerMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task-list")
