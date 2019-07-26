from django.urls import include, path


urlpatterns = [path("api/", include("tests.router", namespace="api"))]
