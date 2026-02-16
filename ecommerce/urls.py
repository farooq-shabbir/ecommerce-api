from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.views import APIView
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token

class RootView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Ecommerce API',
            'endpoints': {
                'products': '/api/products/products/',
                'categories': '/api/products/categories/',
                'orders': '/api/orders/orders/',
                'admin': '/admin/',
                'token': '/api-token-auth/',
            }
        })

urlpatterns = [
    path('', RootView.as_view()),  # Add this
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)