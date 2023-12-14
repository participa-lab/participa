from django.contrib import admin
from .models import Instance, Conversation, Territory, Affinity, Participant


class InstanceAdmin(admin.ModelAdmin):
    pass

class ConversationAdmin(admin.ModelAdmin):
    pass

class TerritoryAdmin(admin.ModelAdmin):
    pass

class AffinityAdmin(admin.ModelAdmin):
    pass

class ParticipantAdmin(admin.ModelAdmin):
    pass


admin.site.register(Instance, InstanceAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Territory, TerritoryAdmin)
admin.site.register(Affinity, AffinityAdmin)
admin.site.register(Participant, ParticipantAdmin)
