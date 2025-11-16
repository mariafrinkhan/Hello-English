from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser, AllowAny
from quiz.permissions import *
# Create your views here.
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    permission_classes = [AllowAny]

    # def get_permissions(self):
    #     if self.request.method in ['GET']:  # list + retrieve
    #         permission_classes = [IsAuthenticated, IsStudent | IsInstructor]
    #     else:  # POST, PUT, PATCH, DELETE
    #         permission_classes = [IsAuthenticated, IsInstructor]
    #     return [p() for p in permission_classes]

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [AllowAny]