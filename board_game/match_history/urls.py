from django.urls import path
from board_game.match_history.views import MatchesHistory

urlpatterns = [
        path('match-history/', MatchesHistory.as_view(),),
        path('match-history/<int:userId>', MatchesHistory.as_view(),name='match-history'),
        path('match-history/<int:gameId>', MatchesHistory.as_view(),name='match-history'),
        path('match-history/<int:userId>/<int:gameId>', MatchesHistory.as_view(),name='match-history'),
]

