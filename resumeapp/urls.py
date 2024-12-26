from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_form, name='resume_form'),
    path("generating-resume/", views.generating_resume, name="generating_resume"),
    path("start-generation/", views.start_generation, name="start_generation"),
    path("download-finished/<str:filename>/", views.download_finished, name="download_finished"),
    path("portfolio/", views.portfolio_view, name="portfolio_view"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)