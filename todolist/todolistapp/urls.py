from django.urls import path

from . import views

app_name="todolistapp"
urlpatterns = [
    path('', views.top),
    path('list/', views.showtasklist, name='list'),
    path('new/', views.makenewtask, name='new'),
    path('register/',views.registertask, name='reg'),
    path('delete/', views.deletetask, name='del'),

]