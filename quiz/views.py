from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser, AllowAny
from .permissions import *


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]


    # def get_permissions(self):
    #     if self.request.method in ['GET']:  # list + retrieve
    #         permission_classes = [IsAuthenticated, IsStudent | IsInstructor]
    #     else:  # POST, PUT, PATCH, DELETE
    #         permission_classes = [IsAuthenticated, IsInstructor]
    #     return [p() for p in permission_classes]

# class InstructionViewSet(viewsets.ModelViewSet):
#     queryset = Instruction.objects.all()
#     serializer_class = InstructionSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         quiz_id = self.request.query_params.get('quiz')
#         if quiz_id:
#             queryset = queryset.filter(quiz_id=quiz_id).order_by('page_en')
#         return queryset


# class InstructionViewSet(viewsets.ModelViewSet):
#     queryset = Instruction.objects.all()
#     serializer_class = InstructionSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         quiz_id = self.request.query_params.get('quiz')
#         if quiz_id:
#             queryset = queryset.filter(quiz=quiz_id).order_by('page')  # use 'quiz' and 'page'
#         return queryset
    

#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         quiz_id = request.query_params.get('quiz')
#         if quiz_id:
#             response.data = {
#                 "total_instructions": self.get_queryset().count(),
#                 "instructions": response.data
#             }
#         return response

class InstructionViewSet(viewsets.ModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        quiz_id = self.request.query_params.get('quiz')
        if quiz_id:
            queryset = queryset.filter(quiz=quiz_id).order_by('page')
        return queryset
    
    permission_classes = [AllowAny]
    
    # def get_permissions(self):
    #     if self.request.method in ['GET']:  # list + retrieve
    #         permission_classes = [IsAuthenticated, IsStudent | IsInstructor]
    #     else:  # POST, PUT, PATCH, DELETE
    #         permission_classes = [IsAuthenticated, IsInstructor]
    #     return [p() for p in permission_classes]




class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    # permission_classes = [AllowAny]

    # def get_permissions(self):
    #     if self.request.method in ['GET']:  # list + retrieve
    #         permission_classes = [IsAuthenticated, IsStudent | IsInstructor]
    #     else:  # POST, PUT, PATCH, DELETE
    #         permission_classes = [IsAuthenticated, IsInstructor]
    #     return [p() for p in permission_classes]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            # GET, HEAD, OPTIONS
            if self.request.user.is_authenticated:
                # Authenticated user can view
                return [IsAuthenticated()]
            else:
                # Unauthenticated user can view
                return [AllowAny()]
        else:
            # POST, PUT, PATCH, DELETE → only admin
            return [IsAdminUser()]

    
    

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    permission_classes = [AllowAny]

    # def get_permissions(self):
    #     if self.request.method in ['GET']:  # list + retrieve
    #         permission_classes = [IsAuthenticated, IsStudent | IsInstructor]
    #     else:  # POST, PUT, PATCH, DELETE
    #         permission_classes = [IsAuthenticated, IsInstructor]
    #     return [p() for p in permission_classes]

    


class GetQuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return QuizListSerializer  # list view: no questions
        return QuizDetailSerializer  # retrieve, create, update, delete
    
    permission_classes = [AllowAny]
    
    # def get_permissions(self):
    #     if self.request.method in ['GET']:  # list + retrieve
    #         permission_classes = [IsAuthenticated, IsStudent | IsInstructor]
    #     else:  # POST, PUT, PATCH, DELETE
    #         permission_classes = [IsAuthenticated, IsInstructor]
    #     return [p() for p in permission_classes]

    



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