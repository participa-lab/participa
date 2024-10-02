from django.urls import path
from polis import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path(
        "c/<str:slug>",
        views.PolisConversationHomeView.as_view(),
        name="conversation_home",
    ),
    path(
        "c/p/<str:slug>",
        views.PolisConversationView.as_view(),
        name="conversation",
    ),
    path(
        "c/r/<str:slug>",
        views.PolisConversationReportView.as_view(),
        name="conversation_report",
    ),
    path(
        "p",
        views.ParticipantView.as_view(),
        name="participant_create",
    ),
    path(
        "p/update/<uuid:pk>",
        views.ParticipantUpdateView.as_view(),
        name="participant_update",
    ),
    path(
        "p/logout",
        views.LogoutView.as_view(),
        name="participant_logout",
    ),
    path("c", views.HomeView.as_view(), name="home"),
    path(
        "about",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about_polis",
    ),
]
