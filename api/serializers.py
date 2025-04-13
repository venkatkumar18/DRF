from rest_framework import serializers
from api.models import Product, Order, User, OrderItem
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock'
        )
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Product Price Must Be Greater Than 0")
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    #product = ProductSerializer()
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal"
        )

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.product.price * order_item.quantity for order_item in order_items)
    
    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "created_at",
            "status",
            'items',
            'total_price',
        )

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerialzier(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity")
    
    items = OrderItemCreateSerialzier(many=True, required=False)
    order_id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        items = validated_data.pop("items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item in items:
                OrderItem.objects.create(order=order, **item)
            return order

    def update(self, instance, validated_data):
        items = validated_data.pop("items") if validated_data.get("items") else None
        with transaction.atomic():
            order = super().update(instance, validated_data)

            if items is not None:
                order.items.all().delete()
                for item in items:
                    OrderItem.objects.create(order=order, **item)
            return order
    
    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            'items',
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }
    
class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password", "groups", "user_permissions")
    