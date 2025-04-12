from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("products/", views.ProductListCreateView.as_view()),
    # path("products/create", views.ProductCreateApiView.as_view()),
    path("products/info/", views.ProductInfoAPIView.as_view()),
    path("products/<int:product_id>/",views.ProductDetailApiView.as_view()),
    path("orders/", views.OrderListApiView.as_view()),
    path("user-orders/", views.UserOrderListApiView.as_view(),name='user-orders')
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]