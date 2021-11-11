from django.urls import path
from .views import Home, file_request

app_name = 'base'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('file', file_request, name='file')
]
