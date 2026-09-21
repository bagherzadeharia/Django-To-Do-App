from todo.forms import *
from typing import override
from todo.models import Task
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import CreateView, FormView, DetailView, ListView, UpdateView, DeleteView

class ToDoListView(LoginRequiredMixin, ListView):
    template_name = 'todo/index.html'
    login_url = '/accounts/login'
    context_object_name = 'tasks'
    # queryset = Task.objects.filter(user=request.user)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(
            user=self.request.user
        )
        context['incomplete_tasks'] = user_tasks.filter(complete=False)
        context['completed_tasks'] = user_tasks.filter(complete=True)
        context['total_tasks'] = user_tasks.count()
        return context

class ToDoCheckView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login'
    model = Task
    success_url = reverse_lazy('todo:list')

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['id'])
        print(task)
        if not task.complete:
            task.complete = True
        else:
            task.complete = False

        task.save()
        return redirect(self.success_url)

class ToDoEditView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login'
    model = Task
    success_url = reverse_lazy('todo:list')
    template_name = 'todo/edit-task.html'
    form_class = TaskForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     task = get_object_or_404(Task, id=kwargs['id'])
    #     context['task'] = Task
    #     return context

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['pk'])
        if request.user != task.user:
            raise PermissionDenied("Access Denied")
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['pk'])
        if request.user != task.user:
            raise PermissionDenied("Access Denied")
        else:
            return super().post(request, *args, **kwargs)

class ToDoDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login'
    model = Task
    success_url = reverse_lazy('todo:list')

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['id'])
        task.delete()
        return redirect(self.success_url)

class ToDoCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    model = Task
    success_url = reverse_lazy('todo:list')
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid")
        return redirect('todo:list')