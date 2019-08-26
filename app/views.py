# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView
from app.models import Task


class TaskList(ListView):
    model = Task


class TaskCreate(CreateView):
    model = Task
    fields = ['name', 'user', 'priority']
    success_url = reverse_lazy('task-list')


class TaskUpdate(UpdateView):
    model = Task
    fields = ['name', 'user', 'priority', 'done']
    success_url = reverse_lazy('task-list')
