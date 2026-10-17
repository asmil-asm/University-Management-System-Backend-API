from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .responder import answer_query
from .serializers import ChatMessageSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_ask(request):
    serializer = ChatMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = answer_query(
        serializer.validated_data['message'],
        locale=serializer.validated_data.get('locale', 'ar'),
    )
    return Response(result)
