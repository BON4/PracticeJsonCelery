from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import UserUpdateForm, UserCreateForm, TextSendForm
from .models import User
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from .tasks import one_sending, mass_sending
from celery import current_app


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
        elif task.status == 'FAILURE':
                response_data['task_status'] = 'FAILURE'

        return JsonResponse(response_data)


    def post(self, request):
        data = {}
        form = TextSendForm(request.POST)

        if form.is_valid():
            json_data = request.POST.dict()
            text = json_data['text']
            del json_data['text']
            task = object
            users_array = []
            for i in json_data:
                users_array.append(json_data[i])

            users_array_reshaped = [users_array[i:i + 2] for i in range(0, len(users_array), 2)]
            print(users_array_reshaped)
            try:
                if len(users_array_reshaped) == 1:
                    task = one_sending.delay(users_array_reshaped[0][0], users_array_reshaped[0][1], text)
                elif len(users_array_reshaped) > 1:
                    a = [x[1] for x in users_array_reshaped]
                    print(a)
                    task = mass_sending.delay(a, text)
            except:
                print("Error in task delaying.")

            data['task_id'] = task.id
            data['task_status'] = task.status
            return JsonResponse(data)

        data['form'] = form
        return JsonResponse(data)

# Create your views here.
