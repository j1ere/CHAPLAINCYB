from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .services.rss_service import fetch_catholic_news


class CatholicNewsAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            posts = fetch_catholic_news(limit=6)
            return Response(posts, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to fetch news", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )