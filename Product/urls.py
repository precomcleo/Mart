from django.conf.urls import url
from django.urls import path, include
from . import views    

app_name = 'PRODUCT'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order_create', views.order_create, name='order_create'), 
    url(r'^(?P<pk>\d+)/delete/$', views.order_delete, name='order_delete'),
    path('top_three', views.top_three, name='top_three'), 
    path('job_function', views.job_function, name='job_function'), 
    ]