from django.shortcuts import render
import django.http as http
from django.urls import reverse
from todolistapp.models import Task
import datetime
# Create your views here.
def top(req):
    # ?
    return HttpResponse("Welcome")
    
def showtasklist(req):
    tasks=Task.objects.all()
    return render(req,'todolistapp/tasklist.html',{'tasks':tasks})

def makenewtask(req):
    # show task registration form
    tasks=Task.objects.all()
    return render(req, 'todolistapp/newtask.html',{'tasks':tasks})

def registertask(req):
    # register task
    keys=["dl_y","dl_mon","dl_d","dl_h","dl_min"]
    prop={
        'taskname':req.POST['taskname'],
        'deadline':datetime.datetime(*map(int,[req.POST[k] for k in keys])),
        'priority':int(req.POST['priority']),
        'do_repeat':'repeat' in req.POST,
        'interval_type':int(req.POST['itvltype']),
        'interval':datetime.timedelta(day=int(req.POST['interval'])) if req.POST['itvltype']=="-1" else None,
        'parent':Task.objects.get(pk=int(req.POST['parent'])) if req.POST['parent']!=-1 else None,
        }
        
    t=Task(**prop)
    t.save()

    return http.HttpResponseRedirect(reverse("todolistapp:list"))

def deletetask(req):
    # delete task
    return http.HttpResponseRedirect(reverse("todolistapp:list"))


