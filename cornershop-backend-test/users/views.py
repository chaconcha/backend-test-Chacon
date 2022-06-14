from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

"""
This file contains "frontend" and "backend" endpoints
for the users authentication.
"""


def loginView(request):
    # Vue form for users login
    return render(request, "login.html")


@api_view(["post"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def auth_login(request, *args, **kwargs):
    # Checks user's username and password,
    # if correct, an Auth Token is created for the user
    try:
        user = User.objects.get(username=request.data.get("username"))
    except User.DoesNotExist:
        return Response(status=401)
    if user.check_password(request.data.get("password")):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": str(token)}, status=200)
    else:
        return Response(status=401)
