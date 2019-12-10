from django import template
register=template.Library()

@register.filter()
def duration(v):
	d_raw=v.days

	w=d_raw//7
	d=d_raw%7

	dsuf="s" if d>1 else ""
	wsuf="s" if w>1 else ""

	dstr="%d day%s"%(d,dsuf) if d>0 else ""
	wstr="%d week%s"%(w,wsuf) if w>0 else ""

	return "%s %s"%(wstr,dstr)