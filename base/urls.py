from django.urls import path
from .views import ModularLocalView, file_request, LocalizationView, HomeView, DocumentationListView, DocumentationView

app_name = 'base'

urlpatterns = [

    path('documentations', DocumentationListView.as_view(), name='documentation-list'),
    path('documentation/<slug:slug>/', DocumentationView.as_view(), name='documentation'),
    path('modular_local/', ModularLocalView.as_view(), name='modular-local'),
    path('localization/', LocalizationView.as_view(), name='localization'),
    path('', HomeView.as_view(), name='home'),
    path('file/', file_request, name='file')
]
