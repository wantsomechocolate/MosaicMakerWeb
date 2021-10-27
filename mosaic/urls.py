from django.urls import path
from . import views

urlpatterns = [
    path('', views.mosaic_index, name='mosaic_index'),
    #path('<mosaic_name>/', views.mosaic_view, name = 'mosaic_view'),
    path('mosaic_detail/<mosaic_name>', views.mosaic_detail, name = 'mosaic_detail'),   ] 