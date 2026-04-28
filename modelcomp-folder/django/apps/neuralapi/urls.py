from apps.neuralapi.api import MachineViewSet, ExerciseViewSet

from rest_framework import routers

router = routers.DefaultRouter()

router.register('neural/machines', MachineViewSet, 'machines')
router.register('neural/exercises', ExerciseViewSet, 'exercises')

urlpatterns = router.urls