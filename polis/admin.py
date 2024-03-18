from django.contrib import admin

from .models import (
    Affinity,
    Conversation,
    Instance,
    Participant,
    PolisConversation,
    PolisParticipant,
    PolisUser,
    PolisXid,
    Territory,
)


class GenericAdmin(admin.ModelAdmin):
    pass


admin.site.register(Instance, GenericAdmin)
admin.site.register(Conversation, GenericAdmin)
admin.site.register(Territory, GenericAdmin)
admin.site.register(Affinity, GenericAdmin)
admin.site.register(Participant, GenericAdmin)
admin.site.register(PolisConversation, GenericAdmin)
admin.site.register(PolisUser, GenericAdmin)
admin.site.register(PolisParticipant, GenericAdmin)
admin.site.register(PolisXid, GenericAdmin)
