from django.urls import path
from .views      import MenuView, Sub_categoryView, CategoryView, ImageView, ProductView

urlpatterns = [
    path('/menu', MenuView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/sub-category', Sub_categoryView.as_view()),
    path('/product', ProductView.as_view()),
    path('/image', ImageView.as_view()),
]