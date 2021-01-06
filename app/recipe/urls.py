from django.urls import path, include
from rest_framework.routers import SimpleRouter

from recipe import views

router = SimpleRouter()

router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
