import logging

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import ParticipantForm
from .models import Conversation, Participant

logger = logging.getLogger(__name__)


class ParticipantMixin(object):
    participant = None
    authenticated_user = None

    def get_from_cookies(self, request):
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                return Participant.objects.get(id=participant_id)
            except Participant.DoesNotExist:
                return None
        return None

    def get_from_user(self, user):
        if user and user.is_authenticated:
            try:
                return Participant.objects.get(user=user)
            except Participant.DoesNotExist:
                return None
        return None

    def init_participant(self, request):
        self.authenticated_user = (
            request.user if request.user and request.user.is_authenticated else None
        )
        user_participant = self.get_from_user(self.authenticated_user)
        cookie_participant = self.get_from_cookies(request)
        logger.info(
            f"authenticated_user: {self.authenticated_user}, user_participant: {user_participant}, cookie_participant: {cookie_participant}"
        )

        if self.authenticated_user and user_participant and cookie_participant:
            logger.info("User is authenticated and has a participant_id cookie")
            if user_participant != cookie_participant:
                logger.info(
                    "User is authenticated and has a different participant_id cookie"
                )
                # If the user is logged in and has a different participant_id cookie, we delete the cookie
                response = HttpResponseRedirect(reverse("home"))
                response.delete_cookie("participant_id")
                return response
            else:
                self.participant = user_participant
        elif self.authenticated_user and cookie_participant:
            logger.info("User is authenticated and has a participant_id cookie")
            # The participant started the conversation without being logged in and now logs in
            self.participant = cookie_participant
            self.participant.assign_user(self.authenticated_user)
        elif self.authenticated_user and user_participant:
            logger.info("User is authenticated and has a participant")
            self.participant = user_participant
        elif cookie_participant:
            logger.info("User is not authenticated and has a participant_id cookie")
            self.participant = cookie_participant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant"] = self.participant
        return context


class HomeView(ParticipantMixin, ListView):
    template_name = "pages/home.html"
    model = Conversation

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        print(self.participant)
        if not self.participant:
            return redirect("participant")

        return super().get(request, *args, **kwargs)


class ParticipantView(ParticipantMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "pages/participant_form.html"

    def get_initial(self):
        initial = super().get_initial()
        if self.participant and self.participant.user:
            initial["name"] = self.participant.user.get_full_name()
            initial["email"] = self.participant.user.email
        return initial

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        if self.participant:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        participant = form.save()
        logger.info(f"Participant created: {participant}")
        current_user = self.request.user
        if current_user.is_authenticated:
            participant.assign_user(current_user)
        if form.data.get("login") == "2":
            response = HttpResponseRedirect(reverse("participant_login"))
        else:
            response = HttpResponseRedirect(
                reverse("home")
            )  # Change to your success URL
        response.set_cookie(
            "participant_id", participant.id, max_age=31536000
        )  # Set a cookie for one year
        return response


class LoginView(TemplateView):
    template_name = "pages/login_form.html"


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponseRedirect(reverse("home"))
        response.delete_cookie("participant_id")
        logout(request)
        return response


class PolisConversationView(ParticipantMixin, DetailView):
    template_name = "pages/conversation.html"
    model = Conversation
    participant = None

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        if not self.participant:
            return redirect("home")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_report"] = True if self.get_object().get_report_url() else False
        return context


class PolisConversationReportView(DetailView):
    template_name = "pages/report.html"
    model = Conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_url"] = self.get_object().get_report_url()
        return context
