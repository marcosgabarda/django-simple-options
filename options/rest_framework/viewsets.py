from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from options.models import Option, UserOption
from options.rest_framework.serializers import OptionSerializer, UserOptionSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = (IsAdminUser,)


class UserOptionViewSet(viewsets.ModelViewSet):
    queryset = UserOption.objects.filter_user_customizable()
    serializer_class = UserOptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
