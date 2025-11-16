from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
#import 
from subscriptions.views import *
from quiz.views import *


router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'subscriptions', UserSubscriptionViewSet, basename='subscription')

# quiz router registrations
router.register('banners', BannerViewSet)
router.register('instructions', InstructionViewSet, basename='instruction')
router.register('quizzes', QuizViewSet, basename='quiz')
router.register('questions', QuestionViewSet, basename='question')
router.register('get_quiz', GetQuizViewSet, basename='get_quiz')
router.register('questions_multi', QuestionBulkViewSet, basename='question-bulk')


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('authentication.urls')),
    # path('api/', include('quiz.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # path('api/', include('subscriptions.urls')),
    # include the DRF router declared above (use the router object, not a module named 'router')
    

    
    path('api/', include(router.urls)),
    path('api/', include('authentication.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # static urls for media files
