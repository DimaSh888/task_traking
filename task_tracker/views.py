from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Task, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import TaskForm, TaskFlterForm, CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()

            return redirect("task-detail", pk=comment.task.pk)


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


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.task.pk})


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ["content"]

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.task.pk})
