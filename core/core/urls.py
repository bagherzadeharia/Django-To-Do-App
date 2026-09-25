"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.renderers import SwaggerJSONRenderer
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

schemaView = get_schema_view(
    openapi.Info(
        title="To-Do App API",
        default_version='v1',
        description="Testing the API of my Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="Apache License v2.0"),
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('todo.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("swagger/output.json", schemaView.as_view(renderer_classes=[SwaggerJSONRenderer]), name="schema-json"),
    path("swagger/", schemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)