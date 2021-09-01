from board_game.match_history.optional_serializers.OptionalSerializer import OptionalSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class MatchesHistory(APIView):
    def get(self, request):
        request = request.GET
        serializer = OptionalSerializer(request)
        data = serializer.check_number_of_keys()
        return Response(data)


