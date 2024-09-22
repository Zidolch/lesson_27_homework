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
from users.models import User, Location


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'age': user.age,
            'locations': [location.name for location in user.location_id.all()],
            'total_ads': user.ad_set.filter(is_published=True).count(),
            })


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        users = []
        for user in page_obj:
            users.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'age': user.age,
                'locations': [location.name for location in user.locations.all()],
                'total_ads': user.ad_set.filter(is_published=True).count(),
            })

        result = {
            'items': users,
            'total': paginator.count,
            'num_pages': paginator.num_pages
        }

        return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        new_user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
        )

        for loc in user_data.get('locations'):
            location, _ = Location.objects.get_or_create(name=loc)
            new_user.locations.add(location)

        return JsonResponse({
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'age': new_user.age,
            'locations': [location.name for location in new_user.locations.all()],
            'total_ads': new_user.ad_set.filter(is_published=True).count(),
            }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        if 'username' in user_data:
            self.object.username = user_data['username']
        if 'password' in user_data:
            self.object.password = user_data['password']
        if 'first_name' in user_data:
            self.object.first_name = user_data['first_name']
        if 'last_name' in user_data:
            self.object.last_name = user_data['last_name']
        if 'age' in user_data:
            self.object.age = user_data['age']
        if 'locations' in user_data:
            for loc in user_data.get('locations'):
                location, _ = Location.objects.get_or_create(name=loc)
                self.object.locations.add(location)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
            'age': self.object.age,
            'locations': [location.name for location in self.object.locations.all()],
            'total_ads': self.object.ad_set.filter(is_published=True).count(),
            }, status=201)



@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)