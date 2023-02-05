from django.conf.urls.static import static
from django.urls import path

from ads.views.ad import *
from lesson_31_homework import settings

urlpatterns = [
    # path('', AdListView.as_view()),
    # path('<int:pk>/', AdDetailView.as_view()),
    # path('create/', AdCreateView.as_view()),
    # path('<int:pk>/update/', AdUpdateView.as_view()),
    # path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdImageView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
