from django.contrib import admin
from board_game.models import Project,Game,User,Player,Match

admin.site.register(Project)
admin.site.register(Game)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username')
    search_fields = ('id','username')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id','game','maxPlayers')
    search_fields = ('id','game','maxPlayers')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('match','playerName')
    search_fields = ('match','playerName')
# admin.site.register(Match)


# Register your models here.
