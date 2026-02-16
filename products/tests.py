from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Category, Product
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        self.user.is_staff = True
        self.user.save()
        
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)  # Use this instead
        
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic items'
        )
        self.product = Product.objects.create(
            name='Laptop',
            slug='laptop',
            description='A powerful laptop',
            price=999.99,
            category=self.category,
            created_by=self.user
        )

    def test_product_list(self):
        response = self.client.get('/api/products/products/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_product(self):
        data = {
            'name': 'Phone',
            'slug': 'phone',
            'description': 'Smart phone',
            'price': 599.99,
            'category_id': self.category.id,
        }
        response = self.client.post('/api/products/products/', data)
        if response.status_code != 201:
            print(f"\nStatus: {response.status_code}")
            print(f"Data: {response.data}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_filter_by_category(self):
        response = self.client.get(f'/api/products/products/?category={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_product(self):
        response = self.client.get('/api/products/products/?search=laptop')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)