from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from levelupapi.views import register_user, login_user, EventView, GameView, GameTypeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')
router.register(r'gametypes', GameTypeView, 'gametype')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_user),
    path('register', register_user),
    path('', include(router.urls)),
    path('', include('levelupreports.urls')),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

