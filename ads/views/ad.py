from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.permissions import IsAdOwnerOrStaff
from ads.serializers import *


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    default_serializer = AdSerializer
    serializer_classes = {
        'list': AdListSerializer,
        'retrieve': AdDetailSerializer,
        'create': AdCreateSerializer,
    }

    default_permission = [AllowAny()]
    permissions = {
        'retrieve': [IsAuthenticated()],
        'create': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsAdOwnerOrStaff()],
        'partial_update': [IsAuthenticated(), IsAdOwnerOrStaff()],
        'delete': [IsAuthenticated(), IsAdOwnerOrStaff()],
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        locations = request.GET.get('location')
        if locations:
            self.queryset = self.queryset.filter(author__locations__name__icontains=locations)

        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'address': [location.name for location in self.object.author.locations.all()],
            'is_published': self.object.is_published,
            'category_id': self.object.category.name,
            'image': self.object.image.url if self.object.image else None,
        }, status=201)
