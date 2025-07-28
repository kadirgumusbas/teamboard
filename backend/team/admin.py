from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'owner__username', 'members__username')
    filter_horizontal = ('members',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Takım sahibi daima üye olsun
        if obj.owner and obj.owner not in obj.members.all():
            obj.members.add(obj.owner)

admin.site.register(Team, TeamAdmin)