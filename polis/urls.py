from django.urls import path, include
from polis import views

urlpatterns = [
    path('', views.participant_view, name='participant'),
    path("__reload__/", include("django_browser_reload.urls")),
]

