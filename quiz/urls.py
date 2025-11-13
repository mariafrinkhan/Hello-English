from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('banners', BannerViewSet)
router.register('instructions', InstructionViewSet, basename='instruction')
router.register('quizzes', QuizViewSet, basename='quiz')
router.register('questions', QuestionViewSet, basename='question')
router.register('get_quiz', GetQuizViewSet, basename='get_quiz')
router.register('subscriptions', PlanViewSet, basename='plan')



urlpatterns = [
    path('', include(router.urls) )
]

