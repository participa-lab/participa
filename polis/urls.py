from django.urls import include, path
from django.http import HttpResponse
from polis import views


urlpatterns = [
    path(
        "polis/<str:slug>",
        views.PolisConversationView.as_view(),
        name="conversation",
    ),
    path(
        "polis/report/<str:slug>",
        views.PolisConversationReportView.as_view(),
        name="conversation_report",
    ),
    path(
        "participant",
        views.ParticipantView.as_view(),
        name="participant",
    ),
    path(
        "participant/login",
        views.LoginView.as_view(),
        name="participant_login",
    ),
    path(
        "participant/logout",
        views.LogoutView.as_view(),
        name="participant_logout",
    ),
    path("healthcheck/", lambda r: HttpResponse()),
    path("", views.HomeView.as_view(), name="home"),
    path("__reload__/", include("django_browser_reload.urls")),
]
