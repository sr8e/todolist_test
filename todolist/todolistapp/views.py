from django.shortcuts import render
import django.http as http
from django.urls import reverse
from todolistapp.models import Task
# Create your views here.
def top(req):
    # ?
    return HttpResponse("Welcome")

def showtasklist(req):
    tasks=Task.objects.all
    return render(req,'todolistapp/tasklist.html',{'tasks':tasks})

def makenewtask(req):
    # show task registration form
    return http.HttpResponse("new task")

def registertask(req):
    # register task
    return http.HttpResponseRedirect(reverse("todolistapp:list"))

def deletetask(req):
    # delete task
    return http.HttpResponseRedirect(reverse("todolistapp:list"))


