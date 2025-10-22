from rest_framework.routers import DefaultRouter
from .views import ChecklistViewSet, ChecklistItemViewSet

router = DefaultRouter()
router.register(r'checklists', ChecklistViewSet)
router.register(r'items', ChecklistItemViewSet)

urlpatterns = router.urls
