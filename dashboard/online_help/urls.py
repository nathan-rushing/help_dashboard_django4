from django.urls import path
from . import views

app_name = 'online_help'

urlpatterns = [
    path("home_test/", views.home_test, name="home_test"),
    path("tasks_test/", views.tasks_test, name="tasks_test"),
    path("documents/", views.document_list, name="document_list"),
    path("documents/<int:document_id>/", views.document_sections, name="document_sections"),
    path("sections/<int:section_id>/", views.section_subsections, name="section_subsections"),
    path("subsections/<int:subsection_id>/", views.subsection_details, name="subsection_details"),
]
