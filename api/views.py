from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilter, OrderFiler, ProductFilter
from api.models import Order, OrderItem, Product, User
from rest_framework.throttling import ScopedRateThrottle
from api.tasks import send_mail_on_order_creation

from .serializers import *


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
    pagination_class.page_size = 10
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 4
    throttle_scope = 'products'
    throttle_classes = [ScopedRateThrottle]

    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()  


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
    throttle_scope = 'orders'
    throttle_classes = [ScopedRateThrottle]

    @method_decorator(cache_page(60 * 15, key_prefix='order_list'))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)  

    def get_queryset(self):
        import time
        time.sleep(2)
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        send_mail_on_order_creation.delay(order.order_id, self.request.user.email)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]


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