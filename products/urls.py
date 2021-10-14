from django.urls import path
from .views      import ProductsView, SizeView, ImageView, ProductView

urlpatterns = [
    path('/menu', ProductsView.as_view()),
    path('/product', ProductView.as_view()),
    path('/image', ImageView.as_view()),
    path('/size', SizeView.as_view()),
]