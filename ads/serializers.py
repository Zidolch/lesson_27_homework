from rest_framework import serializers

from ads.models import Ad, Category
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Ad
        fields = '__all__'
