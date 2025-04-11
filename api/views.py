from django.shortcuts import render
from .serializers import *
from django.http import JsonResponse
from api.models import Product, Order, OrderItem, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def product_detail(request, pk):
#     products = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(products)
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related(
#         "items__product"
#     )
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        "products": products,
        "count": len(products),
        "max_price": products.aggregate(max_price=Max("price"))["max_price"]
    })
    return Response(serializer.data)