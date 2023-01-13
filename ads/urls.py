from django.urls import path

from ads.views import root, CategoryView, CategoryDetailView, AdView, AdDetailView

urlpatterns = [
    path('', root),
    path('cat/', CategoryView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('ad/', AdView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
]