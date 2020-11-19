from django.apps import AppConfig

class BoardgameConfig(AppConfig):
    name = 'board_game'
    def ready(self):
        from . import signals
