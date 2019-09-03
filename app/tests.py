from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from unittest.mock import patch
from .models import Priority, Task
from .views import EventList, TaskList

event1 = {'name': 'Test Event 1', 'id': 1}
event2 = {'name': 'Test Event 2', 'id': 2}
event3 = {'name': 'Test Event 3', 'id': 3}
events = [event1, event2, event3]


class ModelTest(TestCase):
    def test_priority_name_uniqueness(self):
        PRIORITY_NAME = 'Name'
        priority1 = Priority(name=PRIORITY_NAME)
        priority1.full_clean()
        priority1.save()
        priority2 = Priority(name=PRIORITY_NAME)
        with self.assertRaises(ValidationError) as cm:
            priority2.full_clean()
        self.assertIn(
            'Priority with this Name already exists.',
            cm.exception.messages)


class ViewTest(TestCase):
    def setUp(self):
        self.priority = Priority.objects.create(name='Low')
        username = 'test_user'
        password = 'test_pass'
        User.objects.create_user(username=username, password=password)
        self.logged_client = Client()
        self.logged_client.login(username=username, password=password)


    def test_event_list_view_returns_200_when_logged(self):
        URL = '/events/'
        with patch('app.views.get_events', return_value=events):
            response = self.logged_client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], EventList.template_name)

    def test_event_list_view_returns_302_when_not_logged(self):
        URL = '/events/'
        client = Client()
        with patch('app.views.get_events', return_value=events):
            response = client.get(URL)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next={}'.format(URL))

    def test_task_list_view_returns_200(self):
        URL = '/events/{}/tasks/'.format(1)
        with patch('app.views.get_event', return_value=event1):
            response = self.logged_client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], TaskList.template_name)

    def test_task_list_view_returns_302_when_not_logged(self):
        client = Client()
        URL = '/events/{}/tasks/'.format(1)
        with patch('app.views.get_event', return_value=events):
            response = client.get(URL)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next={}'.format(URL))

    def test_task_create_view_returns_302(self):
        EVENT_ID = 1
        URL = '/events/{}/tasks/create/'.format(EVENT_ID)
        data = {'name': 'new task', 'priority': '1'}
        response = self.logged_client.post(URL, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/events/{}/tasks/'.format(EVENT_ID))
        event_tasks = Task.objects.filter(event_id=1)
        self.assertEqual(len(event_tasks), 1)
        self.assertEqual(event_tasks[0].name, data['name'])

    def test_task_create_view_redirects_to_login_when_not_logged(self):
        client = Client()
        URL = '/events/{}/tasks/create/'.format(1)
        data = {'name': 'new task', 'priority': '1'}
        response = client.post(URL, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next={}'.format(URL))

    def test_task_update_view_returns_302(self):
        EVENT_ID = 1
        task_data = {
            'name': 'test1',
            'event_id': EVENT_ID,
            'priority': self.priority
        }
        task = Task.objects.create(**task_data)
        URL = '/events/{}/tasks/update/{}/'.format(EVENT_ID, task.id)
        data = {'name': 'new task', 'priority': '1'}
        response = self.logged_client.post(URL, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/events/{}/tasks/'.format(EVENT_ID))
        event_tasks = Task.objects.filter(event_id=EVENT_ID)
        self.assertEqual(len(event_tasks), 1)
        self.assertEqual(event_tasks[0].name, data['name'])

    def test_task_update_view_redirects_to_login_when_not_logged(self):
        client = Client()
        EVENT_ID = 1
        task_data = {
            'name': 'test1',
            'event_id': EVENT_ID,
            'priority': self.priority
        }
        task = Task.objects.create(**task_data)
        URL = '/events/{}/tasks/update/{}/'.format(EVENT_ID, task.id)
        data = {'name': 'new task', 'priority': '1'}
        response = client.post(URL, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next={}'.format(URL))

    def test_task_delete_view_returns_302(self):
        EVENT_ID = 1
        task_data = {
            'name': 'test1',
            'event_id': EVENT_ID,
            'priority': self.priority
        }
        task = Task.objects.create(**task_data)
        URL = '/events/{}/tasks/delete/{}/'.format(EVENT_ID, task.id)
        response = self.logged_client.post(URL, data={'event_id': task.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/events/{}/tasks/'.format(EVENT_ID))
        event_tasks = Task.objects.all()
        self.assertEqual(len(event_tasks), 0)

    def test_task_delete_view_redirects_to_login_when_not_logged(self):
        client = Client()
        EVENT_ID = 1
        task_data = {
            'name': 'test1',
            'event_id': EVENT_ID,
            'priority': self.priority
        }
        task = Task.objects.create(**task_data)
        URL = '/events/{}/tasks/delete/{}/'.format(EVENT_ID, task.id)
        data = {'name': 'new task', 'priority': self.priority}
        response = client.post(URL, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next={}'.format(URL))
        event_tasks = Task.objects.all()
        self.assertEqual(len(event_tasks), 1)

    def test_mark_as_done_view_returns_302(self):
        EVENT_ID = 1
        task_data = {
            'name': 'test1',
            'event_id': EVENT_ID,
            'priority': self.priority
        }
        task = Task.objects.create(**task_data)
        URL = '/events/{}/tasks/done/{}/'.format(EVENT_ID, task.id)
        response = self.logged_client.post(URL, data={'event_id': task.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/events/{}/tasks/'.format(EVENT_ID))
        done_task = Task.objects.get(id=task.id)
        self.assertTrue(done_task.done)

    def test_mark_as_done_view_redirects_to_login_view(self):
        client = Client()
        EVENT_ID = 1
        task_data = {
            'name': 'test1',
            'event_id': EVENT_ID,
            'priority': self.priority
        }
        task = Task.objects.create(**task_data)
        URL = '/events/{}/tasks/done/{}/'.format(EVENT_ID, task.id)
        response = client.post(URL, data={'event_id': task.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next={}'.format(URL))
        done_task = Task.objects.get(id=task.id)
        self.assertFalse(done_task.done)
