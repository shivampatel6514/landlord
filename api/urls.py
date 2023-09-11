from django.urls import path
from . import views
from .views import CreateUserAPIView,UpdateUserAPIView,DeleteUserAPIView,ListUserAPIView,ListTagViewSet
from .views import LoginAPIView,TagViewSet,PropertyViewSet,PropertyTypeViewSet,ListContactViewSet,CreateContactViewSet,ListPropertyTypeViewSet,ListPropertyViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve
from django.views.static import serve
# from django.conf.urls import url
from django.views.static import serve

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'list-tags', ListTagViewSet, basename='list-tag')

router.register(r'propertyType', PropertyTypeViewSet)
router.register(r'list-propertyType', ListPropertyTypeViewSet, basename='list-propertyType')

router.register(r'properties', PropertyViewSet)
router.register(r'list-properties', ListPropertyViewSet ,basename='list-properties')

router.register(r'contacts', ListContactViewSet, basename='list-contact')
router.register(r'create-contact', CreateContactViewSet, basename='create-contact')

urlpatterns = [
    path('', views.index,name="index"),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/', ListUserAPIView.as_view(), name='list-user'),
    path('create/', CreateUserAPIView.as_view(), name='create-user'),
    path('update/<str:user_id>/', UpdateUserAPIView.as_view(), name='update-user'),
    path('user/<str:user_id>/delete/', DeleteUserAPIView.as_view(), name='delete-user'),
    path('api/', include(router.urls)),  # Include the router's URLs
    re_path(r'^property_images/(?P<path>.*)$', serve, {'document_root': 'property_images'}),

]
# sabdajdb