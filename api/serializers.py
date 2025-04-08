from rest_framework import serializers
from api.models import Product, Order, User, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock'
        )
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Product Price Must Be Greater Than 0")
        return value
    