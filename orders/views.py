from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderDetailSerializer, OrderListSerializer
import uuid


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}"
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['pending', 'processing']:
            return Response(
                {'error': 'Order cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'cancelled'
        order.save()
        return Response({'status': 'Order cancelled'})

    @action(detail=True, methods=['post'])
    def mark_shipped(self, request, pk=None):
        order = self.get_object()
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff can update order status'},
                status=status.HTTP_403_FORBIDDEN
            )
        order.status = 'shipped'
        order.save()
        return Response({'status': 'Order marked as shipped'})