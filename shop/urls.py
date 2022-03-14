from django.urls import path
from .views import login, RegisterView, ProductView, ProductViewSet, AaaCartView, ProfilView, History, OrderView

urlpatterns = [
    path('login/', login),
    path('register/', RegisterView.as_view()),
    path('product/<str:category>/', ProductView.as_view()),
    path('detail/<int:pk>/', ProductViewSet.as_view()),
    path('add/card/<int:id>/', AaaCartView.as_view()),
    path('order/', OrderView.as_view()),
    path('profil/<int:id>/', ProfilView.as_view()),
    path('history/<int:id>/', History.as_view())
]
