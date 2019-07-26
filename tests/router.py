from django.urls import include, path
from rest_framework import routers

from options.rest_framework.viewsets import OptionViewSet, UserOptionViewSet


app_name = "api"

router = routers.DefaultRouter()
router.register("options", viewset=OptionViewSet)
router.register("user-options", viewset=UserOptionViewSet)

urlpatterns = [path("", include(router.urls))]
