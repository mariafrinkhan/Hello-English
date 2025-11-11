from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

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




class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    
    

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    


class GetQuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return QuizListSerializer  # list view: no questions
        return QuizDetailSerializer  # retrieve, create, update, delete

    



class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer