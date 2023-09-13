from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet

app_name = 'api'

API_VERSION = 'v1'

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
# router.register('groups', GroupViewSet, basename='group')
# router.register(r'^habits/(?P<habit_id>\d+)/comments',
#                 CommentViewSet, basename='comment')
# router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
# urlpatterns = [
#     path(f'{API_VERSION}/', include(router.urls)),
#     path(f'{API_VERSION}/', include('djoser.urls')),
#     path(f'{API_VERSION}/', include('djoser.urls.jwt')),
# ]
