from . import views
from django.urls import path

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('process/', views.process_file, name='process_file'),
    path('', views.index, name="index")
]