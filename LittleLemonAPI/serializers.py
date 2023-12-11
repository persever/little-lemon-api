import bleach
from decimal import Decimal
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password 
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import Category, MenuItem, Order, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    
    def validate(self, attrs):
        if 'title' in attrs:
            attrs['title'] = bleach.clean(attrs['title'])
        # for attr in attrs:
        #     attrs[attr] = bleach.clean(attrs[attr])

        return super().validate(attrs)

    class Meta:
        model = MenuItem
        fields = ['id', 'category', 'category_id', 'featured', 'price', 'price_after_tax', 'title']
        extra_kwargs = {
            'price': { 'min_value': 2 },
            'title': {
                'validators': [
                    UniqueValidator(queryset=MenuItem.objects.all())
                ]
            }
        }

    def calculate_tax(self, product:MenuItem):
        return round(product.price * Decimal(1.1), 2)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date', 'delivery_crew', 'status', 'total', 'user']

class RatingSerializer(serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField( 
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rating
        fields = ['user', 'menuitem_id', 'rating']
        validators: [UniqueTogetherValidator(
            queryset=Rating.objects.all(),
            fields=['user', 'menuitem_id'],
            message='You already rated that item. No take-backs!'
        )]
        extra_kwargs = {
            'rating': { 'max_value': 5, 'min_value': 0 }
        }