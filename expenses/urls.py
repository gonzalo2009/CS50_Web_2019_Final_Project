from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("expenses", views.expenses_view, name="expenses"),
    path("get_data", views.get_data_view, name="get_data"),
    path("delete_expense/<int:expense_id>", views.delete_expense_view, name="delete_expense"),
    path("forecast", views.forecast_view, name="forecast"),
]