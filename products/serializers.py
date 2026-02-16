from rest_framework import serializers
from .models import Category, Product, Review
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'image', 'products_count', 'created_at']

    def get_products_count(self, obj):
        return obj.products.count()


class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user_username', 'title', 'content', 'rating', 'helpful_count', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'discount_price', 'final_price', 'category_name', 
                  'image', 'quantity', 'rating', 'reviews_count', 'status', 'created_at']

    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_final_price(self, obj):  # Add this method
        return float(obj.final_price)


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'discount_price', 'category', 
                  'category_id', 'quantity', 'image', 'status', 'rating', 'reviews', 
                  'reviews_count', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_by', 'created_at', 'updated_at']

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be positive")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)