from django.shortcuts import render
from .serializers import *
from django.http import JsonResponse
from api.models import Product, Order, OrderItem, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import ProductFilter, InStockFilter, OrderFiler
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.decorators import action


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilter,
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']

    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 4

    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# class ProductCreateApiView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)

# class ProductDetailApiView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_url_kwarg = "product_id"

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFiler
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # @action(detail=False,
    #         methods=["get"],
    #         url_path="user-orders",
    #         permission_classes=[IsAuthenticated])
    # def user_orders(self, request):
    #     queryset = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data) 

# class OrderListApiView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items__product")
#     serializer_class = OrderSerializer
#     pagination_class = LimitOffsetPagination

class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    
class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"]
        })
        return Response(serializer.data)


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

# @api_view(["GET"])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         "products": products,
#         "count": len(products),
#         "max_price": products.aggregate(max_price=Max("price"))["max_price"]
#     })
#     return Response(serializer.data)