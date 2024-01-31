"""
URL configuration for sylvan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from library.views import UserViewSet, ReservationStatusViewSet, LineItemViewSet, ReservationViewSet, DelinquencyViewSet, DecisionPointViewSet, login_view, logout_view
from django.contrib.auth.views import LoginView

# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = [ 'url', 'username', 'email', 'is_staff' ]

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reservationstatus', ReservationStatusViewSet)
router.register(r'lineitem', LineItemViewSet)
router.register(r'reservation', ReservationViewSet)
router.register(r'delinquency', DelinquencyViewSet)
router.register(r'decisionpoint', DecisionPointViewSet)

urlpatterns = [
    path("library/", include("library.urls")),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('accounts/login/', LoginView.as_view(template_name='your_custom_login_template.html'), name='login'),
    # path('accounts/', include('django.contrib.auth.urls'))
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
