from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from eventbrite import Eventbrite
from app.models import Task


class Login(LoginView):
    template_name = 'app/login.html'


class Logout(LogoutView):
    template_name = ''


class EventList(LoginRequiredMixin, TemplateView):
    template_name = 'app/events.html'

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['events'] = get_events(self.request.user)
        return context


class TaskList(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'app/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(event_id=int(self.kwargs['event_id']))

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['event_id'] = self.kwargs['event_id']
        context['event'] = get_event(
            self.request.user,
            self.kwargs['event_id']
        )
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'priority']
    template_name = 'app/task_create.html'

    def get_success_url(self):
        return reverse_lazy('task-list', kwargs=self.kwargs)

    def form_valid(self, form):
        form.instance.event_id = self.kwargs['event_id']
        return super(TaskCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['event_id'] = self.kwargs['event_id']
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'priority', 'done']
    template_name = 'app/task_update.html'

    def get_success_url(self):
        return reverse_lazy(
            'task-list',
            kwargs={'event_id': self.kwargs['event_id']}
            )

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['event_id'] = self.kwargs['event_id']
        return context


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'app/task_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'task-list',
            kwargs={'event_id': self.kwargs['event_id']}
        )


@login_required
def mark_as_done(request, event_id, pk):
    task = Task.objects.get(pk=pk)
    if not task.done:
        task.done = True
        task.save()
    return redirect('task-list', event_id)


def get_events(user):
    social_user = user.social_auth.filter(provider='eventbrite')[0]
    eb = Eventbrite(social_user.access_token)
    events = eb.get('/users/me/events')
    return [event for event in events['events']]


def get_event(user, id):
    social_user = user.social_auth.filter(provider='eventbrite')[0]
    eb = Eventbrite(social_user.access_token)
    event = eb.get_event(id)
    return event
