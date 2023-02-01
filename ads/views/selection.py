from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.permissions import IsSelectionOwner
from ads.serializers import SelectionSerializer, SelectionListSerializer, SelectionDetailSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerializer
    serializer_classes = {
        'list': SelectionListSerializer,
        'retrieve': SelectionDetailSerializer,
    }

    default_permission = [AllowAny()]
    permissions = {
        'create': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsSelectionOwner()],
        'partial_update': [IsAuthenticated(), IsSelectionOwner()],
        'delete': [IsAuthenticated(), IsSelectionOwner()],
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

