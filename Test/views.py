from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import UserForm
from .models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView


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


class UserUpdateView(View):
    def post(self, request, *args, **kwargs):
        data = {}
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            data = {'id': user.id, 'name': user.name, 'email': user.email}
        else:
            data = {'error': 'Form not valid'}

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):

    def post(self, request, *args, **kwargs):
        data = {}
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            data = {'id': user.id, 'name': user.name, 'email': user.email}
        else:
            data = {'error': 'Form not valid'}

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(View):
    def post(self, request, pk):
        print('{0}------------'.format(pk))
        data = {}
        user = User.objects.get(pk=pk)
        if user:
            user.delete()
            data['message'] = 'User deleted'
        else:
            data['message'] = 'Error occurred'

        return JsonResponse(data)


# Create your views here.
