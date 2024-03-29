from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:survey_id>/", views.survey, name="survey"),
    path("result/<int:survey_id>/", views.show_result, name="result"),
]
