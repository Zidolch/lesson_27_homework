import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from lesson_28_homework.settings import TOTAL_ON_PAGE
from users.models import User


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'address': [location.name for location in ad.author.locations.all()],
            'is_published': ad.is_published,
            'category_id': ad.category.name,
            'image': ad.image.url if ad.image else None,
            })


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        ads = []
        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author.username,
                'price': ad.price,
                'description': ad.description,
                'address': [location.name for location in ad.author.locations.all()],
                'is_published': ad.is_published,
                'category_id': ad.category.name,
                'image': ad.image.url if ad.image else None,
            })

        result = {
            'items': ads,
            'total': paginator.count,
            'num_pages': paginator.num_pages
        }

        return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ad_data['author'])
        category = get_object_or_404(Category, pk=ad_data['category'])

        ad = Ad.objects.create(
            name=ad_data['name'],
            author=author,
            price=ad_data['price'],
            description=ad_data['description'],
            category=category,
            is_published=ad_data['is_published'],
        )

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'address': [location.name for location in ad.author.locations.all()],
            'is_published': ad.is_published,
            'category_id': ad.category.name,
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if 'name' in ad_data:
            self.object.name = ad_data['name'],
        if 'author' in ad_data:
            author = get_object_or_404(User, pk=ad_data['author'])
            self.object.author = author,
        if 'price' in ad_data:
            self.object.price = ad_data['price'],
        if 'description' in ad_data:
            self.object.description = ad_data['description'],
        if 'is_published' in ad_data:
            self.object.is_published = ad_data['is_published'],
        if 'category' in ad_data:
            category = get_object_or_404(Category, pk=ad_data['category'])
            self.object.category = category

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

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


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


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
