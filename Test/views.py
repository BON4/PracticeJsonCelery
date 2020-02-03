from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import UserUpdateForm, UserCreateForm, TextSendForm
from .models import User
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from .tasks import test_task
from celery import current_app
from django.template.response import TemplateResponse


class UserDetailView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk)
        response = {}
        response = {'id': user.id, 'name': user.name, 'email': user.email}
        return JsonResponse(response)


class UserListView(View):
    def get(self, request):
        users = list(User.objects.all().values())
        data = []
        for i in users:
            data.append({'id': i['id'], 'name': i['name'], 'email': i['email']})

        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    def post(self, request, *args, **kwargs):
        data = {}
        validating_user = get_object_or_404(User, pk=request.POST['id'])
        form = UserUpdateForm(instance=validating_user, data=request.POST)
        if form.is_valid():
            user = form.save()
            data = {'id': user.id, 'name': user.name, 'email': user.email}
        else:
            print(form.errors)
            data = {'error': 'Form not valid'}

        print(data)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):

    def post(self, request, *args, **kwargs):
        data = {}
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            data = {'id': user.id, 'name': user.name, 'email': user.email}
        else:
            data = {'error': 'Form not valid'}

        print(data)

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(View):
    def post(self, request, pk):
        data = {}
        user = User.objects.get(pk=pk)
        if user:
            user.delete()
            data['message'] = 'User deleted'
        else:
            data['message'] = 'Error occurred'

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(View):

    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}
        print("{0}::::::{1}".format(task.id, task.status))
        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)

    def post(self, request):
        data = {}
        form = TextSendForm(request.POST)

        if form.is_valid():
            text = request.POST['text']
            task = test_task.delay(text)
            data['task_id'] = task.id
            data['task_status'] = task.status
            print("{0}::::::{1}".format(task.id, task.status))
            return JsonResponse(data)
        data['form'] = form
        return JsonResponse(data)


# Create your views here.
