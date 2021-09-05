from django.urls import path
from region import views

urlpatterns = [
    path('regions/', views.region, name="regions"),
    path('regions/<int:pk>', views.putregion, name="api"),
]