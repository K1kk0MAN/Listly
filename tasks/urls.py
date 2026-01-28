from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("create", views.create_list, name="create_list"),
    path("tasklist/<int:list_id>", views.task_list, name="task_list"),
    path("browse", views.public_lists, name="public_lists"),

    path("tasklist/<int:list_id>/add", views.add_item, name="add_item"),
    path("task/toggle/<int:item_id>", views.toggle_item, name="toggle_item"),
    path("task/delete/<int:item_id>", views.delete_item, name="delete_item"),
    path("copy-list/<int:list_id>/", views.copy_list, name="copy_list"),

    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"), 
    path("logout", views.logout_view, name="logout")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

