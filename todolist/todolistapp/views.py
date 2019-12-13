from django.shortcuts import render,get_object_or_404
import django.http as http
from django.urls import reverse
from todolistapp.models import Task
from todolistapp.customutil import checkdue
import datetime
from dateutil.relativedelta import relativedelta


#
class InvalidValueError(Exception):
    def __init__(self,msg):
        self.msg=msg

#
prop_keys=["id","taskname","deadline","priority","do_repeat","interval_type","interval","parent"]



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
    msg=req.GET['msg'] if 'msg' in req.GET else None
    page={"title":"Create","msg":msg}
    context={prop_keys[i]:prop_values[i] for i in range(len(prop_keys))}
    
    return render(req, 'todolistapp/newtask.html',{'t_overdue':t_overdue, 't_intime':t_intime, 'n_overdue':n, 'page':page, 'context':context})

def registertask(req):
    # register task
    now=datetime.datetime.now().astimezone()
    tz=now.tzinfo
    keys=["dl_y","dl_mon","dl_d","dl_h","dl_min"]
    try:
        pk=int(req.POST['pk'])
        if pk!=-1 and pk<1 :raise InvalidValueError("Invalid value(1)")
        
        taskname=req.POST['taskname']
        if taskname=="":raise InvalidValueError("TaskName cannot be empty.")
        
        deadline=datetime.datetime(*map(int,[req.POST[k] for k in keys]),tzinfo=tz)
        if deadline<now:raise InvalidValueError("Deadline should be after current time.")
        
        priority=int(req.POST['priority'])
        if not 0<=priority<=3:raise InvalidValueError("Invalid value(2)")

        do_repeat='repeat' in req.POST

        interval_type=int(req.POST['itvltype'])
        if not -1<=interval_type<=3:raise InvalidValueError("Invalid value(3)")
        
        days=0
        if do_repeat and interval_type==-1 :
            days=int(req.POST['interval'])
            if days<1:raise InvalidValueError("Interval should be positive integer.")

        pid=int(req.POST['parent'])
        if pid!=-1 and not Task.objects.filter(pk=pid).exists():raise InvalidValueError("Invalid value(4)")

        
        prop={
            'taskname': taskname,
            'deadline': deadline,
            'priority': priority,
            'do_repeat':do_repeat,
            'interval_type':interval_type,
            'interval':datetime.timedelta(days=days) if days else None,
            'parent':Task.objects.get(pk=pid) if pid!=-1 else None,
            }
            
        if pk!=-1: Task.objects.update_or_create(pk=pk,defaults=prop)
        else:Task(**prop).save()

        return http.HttpResponseRedirect(reverse("todolistapp:list"))
    except (KeyError,TypeError,ValueError) as e:
        # invalid form
        return http.HttpResponseRedirect(reverse("todolistapp:new"))
    except InvalidValueError as e:
        return http.HttpResponseRedirect("%s?msg=%s"%(reverse("todolistapp:new"),e.msg))
            

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
    task=get_object_or_404(Task,pk=pk)
    now=datetime.datetime.now().astimezone()
    limit=task.deadline.astimezone()
    delta=limit-now

    return render(req, 'todolistapp/viewtask.html',{'task':task,'delta':delta})

