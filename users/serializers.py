from rest_framework import serializers

from users.models import User, Location


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Location.objects.all(),
    )

    class Meta:
        model = User
        exclude = ['password']


class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Location.objects.all(),
    )

    total_ads = serializers.IntegerField()

    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='name',
        queryset=Location.objects.all(),
    )

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)

        new_user.set_password(validated_data['password'])
        new_user.save()

        for loc in self._locations:
            location, _ = Location.objects.get_or_create(name=loc)
            new_user.locations.add(location)
        return new_user

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='name',
        queryset=Location.objects.all(),
    )

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for loc in self._locations:
            location, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(location)
        return user

    class Meta:
        model = User
        exclude = ['password']


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
