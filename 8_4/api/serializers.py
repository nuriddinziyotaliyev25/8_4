from rest_framework import serializers

from .models import Customer, Category, Food, Order


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:customer_detail',
        lookup_field='pk'
    )
    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:category_detail',
        lookup_field='slug'
    )
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Category
        fields = '__all__'


class FoodSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:food_detail',
        lookup_field='slug'
    )
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='api:category_detail',
        lookup_field='slug',
        required=True
    )
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Food
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:order_detail',
        lookup_field='id'
    )
    customer = serializers.HyperlinkedRelatedField(
        queryset=Customer.objects.all(),
        view_name='api:customer_detail',
        lookup_field='pk',
        required=True
    )
    items = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Food.objects.all(),
        view_name='api:food_detail',
        lookup_field='slug'
    )

    class Meta:
        model = Order
        fields = '__all__'
