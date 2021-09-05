from django.urls import path
from state import views

urlpatterns = [
    path('state/', views.state, name="state"),
    path('state/<int:pk>', views.api_state, name="state_api"),
]