from django.shortcuts import render, redirect
from .forms import ParticipantForm
from .models import Participant, Conversation


def home(request):
    return render(request, "pages/home.html", {})


def participant_view(request):
    # Check for a specific cookie to determine if the participant is returning
    participant = None
    if "participant_id" in request.COOKIES:
        participant_id = request.COOKIES["participant_id"]
        try:
            participant = Participant.objects.get(id=participant_id)
            # Load the participant data if found
            form = ParticipantForm(instance=participant)
        except Participant.DoesNotExist:
            form = ParticipantForm()
    else:
        form = ParticipantForm()

    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            response = redirect(
                "participant"
            )  # Redirect to a success page or another view
            response.set_cookie(
                "participant_id", participant.id, max_age=31536000
            )  # Set a cookie for one year
            return response

    conversation = None
    if participant:
        conversation = Conversation.objects.filter(instance=participant.instance).first()
    context = {"form": form, "participant": participant, "conversation": conversation}

    return render(request, "pages/participant.html", context)
