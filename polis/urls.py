from django.urls import path
from polis import views

urlpatterns = [
    path("", views.home, name="home"),
    path('participant/', views.participant_view, name='participant'),
]

