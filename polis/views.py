from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import ParticipantForm
from .models import Conversation, Participant


class HomeView(ListView):
    template_name = "pages/home.html"
    model = Conversation
    participant = None
    form = None

    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        initial = {}
        if current_user.is_authenticated:
            try:
                self.participant = Participant.objects.get(user=current_user)
            except Participant.DoesNotExist:
                pass

            initial["name"] = current_user.get_full_name()
            initial["email"] = current_user.email

        if not self.participant and "participant_id" in request.COOKIES:
            try:
                participant_id = request.COOKIES["participant_id"]
                self.participant = Participant.objects.get(id=participant_id)
                if current_user and current_user.is_authenticated:
                    self.participant.assign_user(current_user)
            except Participant.DoesNotExist:
                pass

        self.form = ParticipantForm(instance=self.participant, initial=initial)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["participant"] = self.participant
        return context


class ParticipantView(CreateView):
    model = Participant
    form_class = ParticipantForm

    def form_valid(self, form):
        participant = form.save()
        current_user = self.request.user
        if current_user.is_authenticated:
            participant.assign_user(current_user)
        response = HttpResponseRedirect(reverse("home"))  # Change to your success URL
        response.set_cookie(
            "participant_id", participant.id, max_age=31536000
        )  # Set a cookie for one year
        return response


class PolisConversationView(DetailView):
    template_name = "pages/conversation.html"
    model = Conversation
    participant = None

    def get(self, request, *args, **kwargs):
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                self.participant = Participant.objects.get(id=participant_id)
            except Participant.DoesNotExist:
                return redirect("home")
        else:
            return redirect("home")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant"] = self.participant
        context["show_report"] = True if self.get_object().get_report_url() else False
        return context


class PolisConversationReportView(DetailView):
    template_name = "pages/report.html"
    model = Conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_url"] = self.get_object().get_report_url()
        return context
