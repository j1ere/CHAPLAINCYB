# theme/views.py
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Theme
from .serializers import ThemeSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    # Custom action to set a theme as active
    def set_active(self, request, pk=None):
        theme = get_object_or_404(Theme, pk=pk)
        theme.is_active = True
        theme.save()
        return Response({"message": f"Theme {theme.year} is now active"}, status=status.HTTP_200_OK)





class PublicActiveThemeView(APIView):
    """Public endpoint - returns only the currently active theme"""
    permission_classes = [AllowAny]

    def get(self, request):
        active_theme = Theme.objects.filter(is_active=True).first()
        
        if not active_theme:
            return Response({
                "message": "No active theme set at the moment",
                "theme": None
            }, status=200)

        serializer = ThemeSerializer(active_theme, context={'request': request})
        return Response({
            "theme": serializer.data
        })