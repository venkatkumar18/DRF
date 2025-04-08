from django.shortcuts import render
from .serializers import ProductSerializer
from django.http import JsonResponse
from api.models import Product, Order, OrderItem, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    products = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(products)
    return Response(serializer.data)