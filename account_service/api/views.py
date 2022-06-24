from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, status, decorators


from .permissions import UserReadWritePermission, AdminPermission
from .serializers import ExtendedUserSerializer, SecureSerializer
from .models import CustomUser

# Create your views here.


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "id": user.pk, "email": user.email})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ("list", "retrieve"):
            serializer_class = SecureSerializer
        else:
            serializer_class = ExtendedUserSerializer
        return serializer_class

    def get_permissions(self):
        if self.action in ("list",):
            permission_classes = [AdminPermission]
        else:
            permission_classes = [UserReadWritePermission]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        is_admin = bool(kwargs.get("account", False))
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            instance.is_staff = is_admin
            instance.is_superuser = False
            instance.save()
            token = Token.objects.get_or_create(user=instance)[0]
            response = {"token": token.key}
        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.is_active = False
        user.save()
        return Response(
            {"detail": f"user '{user.username}' was successfully deleted"},
            status=status.HTTP_200_OK,
        )

    @decorators.action(detail=False, methods=["get"])
    def is_admin(self, request):
        is_admin = request.user.is_staff
        return Response({"is_admin": is_admin}, status=status.HTTP_200_OK)
