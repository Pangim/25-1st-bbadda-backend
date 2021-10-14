from django.urls import path

from orders.views import OrderView, OrderProductView

urlpatterns = [
    path("/order", OrderView.as_view()),
    path("/orderitem", OrderProductView.as_view())
]