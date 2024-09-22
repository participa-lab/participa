import logging

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    FormView,
)

from .forms import ParticipantForm, ContactForm
from .models import Conversation, Participant
from allauth.socialaccount.adapter import get_adapter
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


class ParticipantMixin(object):
    participant = None
    authenticated_user = None

    def get_session_id(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

    def get_from_cookies(self, request):
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                return Participant.objects.get(id=participant_id)
            except Participant.DoesNotExist:
                return None
        return None

    def set_cookie(self, response):
        if self.participant:
            response.set_cookie(
                "participant_id", self.participant.id, max_age=31536000
            )  # Set a cookie for one year
        return response

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

        if self.authenticated_user and user_participant and cookie_participant:
            logger.info(
                "User is authenticated, is returning, and has a participant_id cookie"
            )
            if user_participant != cookie_participant:
                logger.info(
                    "User is authenticated and has a different participant_id cookie, merging participants"
                )
                # merge the two participants
                user_participant.merge(cookie_participant)
                cookie_participant.delete()

            self.participant = user_participant
            self.participant.assign_user(self.authenticated_user)
        elif self.authenticated_user and cookie_participant:
            logger.info(
                "User is authenticated, is new, and has a participant_id cookie"
            )
            # The participant started the conversation without being logged in and now logs in
            self.participant = cookie_participant
            self.participant.assign_user(self.authenticated_user)
        elif self.authenticated_user and user_participant:
            logger.info("User is authenticated and has a participant")
            self.participant = user_participant
        elif cookie_participant:
            logger.info("User is not authenticated and has a participant_id cookie")
            self.participant = cookie_participant

        if self.participant:
            logger.info(f"User {self.participant} wins")
            self.participant.refresh_xid_metadata()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant"] = self.participant
        return context


class MainHomeView(ParticipantMixin, FormView):
    template_name = "main_home.html"
    form_class = ContactForm

    def get_conversaciones(self):
        queryset = Conversation.objects.filter(show_in_list=True)
        return queryset

    def get_success_url(self):
        return reverse("main_home") + "#contacto"

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Mensaje recibido de {name} {email}
            ________________________
            Asunto: {subject}

            {message}
            """
        try:
            send_mail(
                subject=f"Mensaje desde el sitio web: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            messages.error(
                self.request,
                _(
                    f"No se pudo enviar el mensaje, escríbenos a {settings.NOTIFY_EMAIL} "
                ),
            )
            return super().form_invalid(form)
        # success message
        messages.success(self.request, _("Gracias por contactarnos"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conversaciones"] = self.get_conversaciones()
        context["slider_conversaciones"] = len(context["conversaciones"]) > 1
        return context


class HomeView(ParticipantMixin, ListView):
    template_name = "pages/home.html"
    model = Conversation
    ref = None

    def get_queryset(self):
        """
        If ref is provided, try to get the conversation by slug, if not found, get a random conversation that is set to show_in_list=True
        """
        queryset = super().get_queryset()
        if self.ref:
            queryset = queryset.filter(slug=self.ref)
            if len(queryset) == 0:
                queryset = super().get_queryset().filter(show_in_list=True)
        else:
            queryset = queryset.filter(show_in_list=True)
        return queryset

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        self.ref = request.GET.get("ref")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider_conversaciones"] = len(context["object_list"]) > 1
        return context


class ParticipantView(ParticipantMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "pages/participant_form.html"
    next = None

    def get_initial(self):
        initial = super().get_initial()
        if self.participant and self.participant.user:
            initial["name"] = self.participant.user.get_full_name()
            initial["email"] = self.participant.user.email
        return initial

    def get(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        logger.info(f"GET ParticipantView, next: {self.next}")
        self.init_participant(request)
        if self.participant:
            # Consolidated participant, saving into cookies
            if self.next:
                response = redirect(self.next)
            else:
                response = redirect("home")
            return self.set_cookie(response)
        # else create a new one
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        logger.info(f"POST ParticipantView, next: {self.next}")
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        logger.info(f"POST ParticipantView form_invalid: {form.errors}")
        return super().form_invalid(form)

    def form_valid(self, form):
        self.participant = form.save()
        logger.info(
            f"POST ParticipantView created: {self.participant}, next: {self.next}"
        )
        response = HttpResponseRedirect(reverse("home"))  # Change to your success URL
        if self.next:
            response = redirect(self.next)

        # get name login
        name_login = form.data.get("login")
        # name_login has the name of the provider
        # find the provider in the registry
        adapter = get_adapter()
        providers = adapter.list_providers(self.request)

        for provider in providers:
            if provider.name == name_login:
                logger.info(f"Provider: {provider}")
                redirect_url = provider.get_login_url(self.request, next=self.next)
                response = redirect(redirect_url)

        self.set_cookie(response)  # Set a cookie for one year
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ParticipantUpdateView(ParticipantMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "pages/participant_update_form.html"
    next = None

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        self.next = request.GET.get("next")
        if not self.participant or self.get_object() != self.participant:
            logger.info("Participant not found or mismatch, redirecting to home")
            if self.next:
                return redirect(self.next)
            else:
                return redirect("home")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("home")

    def post(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.get_object().refresh_xid_metadata()
        logger.info(f"Participant updated: {self.get_object()}")

        response = HttpResponseRedirect(reverse("home"))  # Change to your success URL
        if self.next:
            response = redirect(self.next)

        # get name login
        name_login = form.data.get("login")
        # name_login has the name of the provider
        # find the provider in the registry
        adapter = get_adapter()
        providers = adapter.list_providers(self.request)

        for provider in providers:
            if provider.name == name_login:
                logger.info(f"Provider: {provider}")
                redirect_url = provider.get_login_url(self.request, next=self.next)
                response = redirect(redirect_url)

        self.set_cookie(response)  # Set a cookie for one year
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(TemplateView):
    template_name = "pages/login_form.html"

    def get_success_url(self):
        return reverse("polis::home")

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie("participant_id", self.participant.id, max_age=31536000)
        logger.info("User logged in, participant_id set in cookie")
        return response


class LogoutView(ParticipantMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponseRedirect(reverse("home"))
        response.delete_cookie("participant_id")
        logout(request)
        logger.info("User logged out, participant_id cookie deleted")
        return response


class PolisConversationView(ParticipantMixin, DetailView):
    template_name = "pages/conversation.html"
    model = Conversation
    participant = None

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        if not self.participant:
            # Add next parameter to redirect to the conversation after login
            response = redirect("participant_create")
            response["Location"] += f"?next={request.path}"
            logger.info("No participant found, redirecting to participant_create")
            return response

        response = super().get(request, *args, **kwargs)
        return self.set_cookie(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_report"] = True if self.get_object().get_report_url() else False
        return context


class PolisConversationHomeView(ParticipantMixin, DetailView):
    template_name = "pages/conversation_home.html"
    model = Conversation


class PolisConversationReportView(DetailView):
    template_name = "pages/report.html"
    model = Conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_url"] = self.get_object().get_report_url()
        return context
