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


class ConversationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("topic",)}


class NotManagedAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Instance, GenericAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Territory, GenericAdmin)
admin.site.register(Affinity, GenericAdmin)
admin.site.register(Participant, GenericAdmin)
admin.site.register(PolisConversation, NotManagedAdmin)
admin.site.register(PolisUser, NotManagedAdmin)
admin.site.register(PolisParticipant, NotManagedAdmin)
admin.site.register(PolisXid, NotManagedAdmin)
