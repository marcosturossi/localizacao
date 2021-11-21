from django.urls import path
from .views import ModularLocalView, file_request, LocalizationView, HomeView

app_name = 'base'

urlpatterns = [
    path('modular_local/', ModularLocalView.as_view(), name='modular_local'),
    path('localization/', LocalizationView.as_view(), name='localization'),
    path('', HomeView.as_view(), name='home'),
    path('file/', file_request, name='file')
]
