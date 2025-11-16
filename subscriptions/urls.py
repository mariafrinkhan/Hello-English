from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'subscriptions', UserSubscriptionViewSet, basename='subscription')

urlpatterns = router.urls
