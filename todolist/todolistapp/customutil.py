import datetime
from dateutil import relativedelta

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