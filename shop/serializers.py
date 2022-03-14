from rest_framework import serializers
from account.models import User
from .models import Book, Cart, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name', 'phone', 'address']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'last_name', 'first_name', 'phone', 'address']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product']


class ProductDetailSerializerMine(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'address']
