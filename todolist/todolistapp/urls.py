from django.urls import path

from . import views

app_name="todolistapp"
urlpatterns = [
    path('', views.top),
    path('list/', views.showtasklist, name='list'),
    path('new/', views.makenewtask, name='new'),
    path('register/',views.registertask, name='reg'),
    path('delete/<int:pk>/', views.deletetask, name='del'),
    path('edit/<int:pk>/',views.edittask, name='edit'),
    path('view/<int:pk>/',views.viewtask, name='view'),

]