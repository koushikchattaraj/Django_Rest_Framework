from django.urls import path
from country import views

urlpatterns = [
    path('country/', views.country, name="country"),
    path('country/<int:pk>', views.api_country, name="api"),
]