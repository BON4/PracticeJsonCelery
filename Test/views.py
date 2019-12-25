from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import random


class HomeView(View):

    def get(self, request):
        context = {}
        return render(request, 'Test/Home.html', context)


class TaskView(View):

    def get(self, request):
        response = {'text': 'Hello World', 'number': random.randint(0, 100)}
        return JsonResponse(response)

# Create your views here.
