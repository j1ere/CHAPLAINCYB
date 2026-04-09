from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Group, GroupImage
from .serializers import GroupSerializer, GroupCreateUpdateSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.prefetch_related('images').all()
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GroupCreateUpdateSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save(created_by=request.user)

        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            GroupImage.objects.create(group=group, image=image, order=i)

        return Response(
            GroupSerializer(group, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()

        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            GroupImage.objects.create(group=group, image=image, order=i)

        return Response(GroupSerializer(group, context={'request': request}).data)


class PublicGroupDetailAPIView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, slug=None):
        group = get_object_or_404(Group, slug=slug)
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data)


class PublicGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.prefetch_related('images').all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()

        group_type = self.request.query_params.get('type')
        year = self.request.query_params.get('year')
        is_alumni = self.request.query_params.get('is_alumni')

        if group_type:
            queryset = queryset.filter(type=group_type)

        if year:
            queryset = queryset.filter(year=year)

        if is_alumni is not None:
            queryset = queryset.filter(is_alumni=is_alumni.lower() == 'true')

        return queryset 