from django.urls import path, include
from . import views

urlpatterns = [
    path("products/", views.ProductListApiView.as_view()),
    path("products/info", views.product_info),
    path("products/<int:product_id>",views.ProductDetailApiView.as_view()),
    path("orders/", views.OrderListApiView.as_view()),
    path("user-orders/", views.UserOrderListApiView.as_view(),name='user-orders')
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]