from django.urls import reverse
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Menu
from .serializers import MenuDetailSerializer, MenuResponseSerializer, MenuSerializer
from .tasks import send_Slack_menu_reminder


class MenuViewSet(viewsets.ModelViewSet):
    """
    ModelViewset creates the following default actions for the Menu instances:
        - list
        - create
        - retrieve
        - update
        - delete
    And defines some custom actions
    """

    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def form(self, request, pk=None):
        # Gets menu data with it's options, that are used for creating a form
        menu = self.get_object()
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def respond(self, request, pk=None):
        # Saves employee's meal choice
        response_data = request.data
        serializer = MenuResponseSerializer(data={**response_data, "menu": pk})

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[TokenAuthentication],
        permission_classes=[permissions.IsAuthenticated],
    )
    def reminder(self, request, pk=None):
        # Sends Slack reminder to employees
        menu_url = request.build_absolute_uri(reverse("menu-response", args=(pk,)))
        send_Slack_menu_reminder.delay(menu_url)
        return Response(status=200)
