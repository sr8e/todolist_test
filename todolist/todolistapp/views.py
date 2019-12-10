from django.shortcuts import render
import django.http as http
from django.urls import reverse
from todolistapp.models import Task
import datetime
from dateutil.relativedelta import relativedelta

#
prop_keys=["id","taskname","deadline","priority","do_repeat","interval_type","interval","parent"]

def checkdue(tasks, pk=-1):
    intervals=[
        {"days":7},{"days":14},{"months":1},{"months":2}
    ]
    now=datetime.datetime.now().astimezone()
    t_overdue=[]
    t_intime=[]
    for t in tasks:
        if t.id==pk:continue
        if t.deadline<now:
            if t.do_repeat:
                tp=t.interval_type
                while t.deadline<now:
                    if tp==-1:
                        t.deadline+=t.interval
                    else:
                        t.deadline+=relativedelta(**intervals[tp])
                t.save()
                t_intime.append(t)
            else:
                t_overdue.append(t)
        else:
            t_intime.append(t)
    return (t_overdue, t_intime, len(t_overdue))

# Create your views here.
def top(req):
    # ?
    return HttpResponse("Welcome")
    
def showtasklist(req):
    tasks=Task.objects.all()
    t_overdue,t_intime,n=checkdue(tasks)
                
                
    return render(req,'todolistapp/tasklist.html',{'t_overdue':t_overdue, 't_intime':t_intime, 'n_overdue':n})

def makenewtask(req):
    # show task registration form
    tasks=Task.objects.all()
    t_overdue,t_intime,n=checkdue(tasks)

    prop_values=[-1,"",None,0,False,-1,"",-1]
    page={"title":"Create",}
    context={prop_keys[i]:prop_values[i] for i in range(len(prop_keys))}
    
    return render(req, 'todolistapp/newtask.html',{'t_overdue':t_overdue, 't_intime':t_intime, 'n_overdue':n, 'page':page, 'context':context})

def registertask(req):
    # register task
    tz=datetime.datetime.now().astimezone().tzinfo
    keys=["dl_y","dl_mon","dl_d","dl_h","dl_min"]
    pk=int(req.POST['pk'])
    prop={
        'taskname':req.POST['taskname'],
        'deadline':datetime.datetime(*map(int,[req.POST[k] for k in keys]),tzinfo=tz),
        'priority':int(req.POST['priority']),
        'do_repeat':'repeat' in req.POST,
        'interval_type':int(req.POST['itvltype']),
        'interval':datetime.timedelta(days=int(req.POST['interval'])) if 'repeat' in req.POST and req.POST['itvltype']=="-1" else None,
        'parent':Task.objects.get(pk=int(req.POST['parent'])) if req.POST['parent']!="-1" else None,
        }
        
    if pk!=-1: Task.objects.update_or_create(pk=pk,defaults=prop)
    else:Task(**prop).save()

    return http.HttpResponseRedirect(reverse("todolistapp:list"))

def deletetask(req,pk):
    # delete task
    Task.objects.filter(pk=pk).delete()
    return http.HttpResponseRedirect(reverse("todolistapp:list"))

def edittask(req,pk):
    tasks=Task.objects.all()
    t_overdue,t_intime,n=checkdue(tasks,pk)

    t=Task.objects.get(pk=pk)
    page={"title":"Edit",}
    
    context={k:getattr(t,k) for k in prop_keys}
    context["deadline"]=context["deadline"].astimezone()

    return render(req, 'todolistapp/newtask.html',{'t_overdue':t_overdue, 't_intime':t_intime, 'n_overdue':n, 'page':page, 'context':context})

def viewtask(req,pk):
    return http.HttpResponse("pk:%d"%pk)

