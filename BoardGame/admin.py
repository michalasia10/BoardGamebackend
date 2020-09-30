from django.contrib import admin
from BoardGame.models import Project,Game,User,Player,Match

admin.site.register(Project)
admin.site.register(Game)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username')
    search_fields = ('id','username')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('game','maxPlayers')
    search_fields = ('game','maxPlayers')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('room','playerName')
    search_fields = ('room','playerName')
# admin.site.register(Match)


# Register your models here.
