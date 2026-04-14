from neural.api import MachineViewSet, ExerciseViewSet

from rest_framework import routers

router = routers.DefaultRouter()

router.register('api/machines', MachineViewSet, 'machines')
router.register('api/exercises', ExerciseViewSet, 'exercises')

urlpatterns = router.urls