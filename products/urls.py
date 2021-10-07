from django.urls import path
from .views      import MenuView, SubCategoryView, CategoryView, ImageView, ProductView

urlpatterns = [
    path('/menu', MenuView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/sub-category', SubCategoryView.as_view()),
    path('/product', ProductView.as_view()),
    path('/image', ImageView.as_view()),
]