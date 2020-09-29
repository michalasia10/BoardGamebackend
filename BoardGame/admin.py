from django.contrib import admin
from BoardGame.models import Project,Game,User,Player,Match

admin.site.register(Project)
admin.site.register(Game)
admin.site.register(User)
# admin.site.register(Player)
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('game','playersNumber')
    search_fields = ('game','playersNumber')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('room','playerName')
    search_fields = ('room','playerName')
# admin.site.register(Match)


# Register your models here.
