from django import template
import todolistapp
from todolistapp.customutil import checkdue

register=template.Library()

@register.inclusion_tag("todolistapp/notify.html")
def disp_notify():
	tasks=todolistapp.models.Task.objects.all()
	t_overdue,t_intime,n=checkdue(tasks)

	return {'t_overdue':t_overdue, 'n':n}

	