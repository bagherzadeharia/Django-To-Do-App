from todo.api.v1.views import TaskModelViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('tasks', TaskModelViewSet, basename='task')

app_name = 'api-v1'

urlpatterns = router.urls