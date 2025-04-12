from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

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

urlpatterns += [
    # YOUR PATTERNS
    path('api/spectacular/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/spectacular/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/spectacular/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('api/yasg/swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('api/yasg/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/yasg/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]