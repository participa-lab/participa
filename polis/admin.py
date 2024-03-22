from django.contrib import admin

from .models import Affinity, Conversation, Instance, Territory


class GenericAdmin(admin.ModelAdmin):
    pass


class ConversationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("topic",)}


admin.site.register(Instance, GenericAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Territory, GenericAdmin)
admin.site.register(Affinity, GenericAdmin)
# admin.site.register(Participant, GenericAdmin)
# admin.site.register(PolisConversation, GenericAdmin)
# admin.site.register(PolisUser, GenericAdmin)
# admin.site.register(PolisParticipant, GenericAdmin)
# admin.site.register(PolisXid, GenericAdmin)
