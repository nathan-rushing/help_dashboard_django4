from django.urls import path
from . import views

app_name = 'online_help'

urlpatterns = [
    path("home_test/", views.home_test, name="home_test"),
    path("tasks_test/", views.tasks_test, name="tasks_test"),
    path("document_list/", views.document_list, name="document_list"),
    path("document_list_edit/", views.document_list_edit, name="document_list_edit"),
    path("documents_sections/<int:document_id>/", views.document_sections, name="document_sections"),
    path("documents_sections_edit/<int:document_id>/", views.document_sections_edit, name="document_sections_edit"),
    path("sections_subsections/<int:section_id>/", views.section_subsections, name="section_subsections"),
    path("sections_subsections_edit/<int:section_id>/", views.section_subsections_edit, name="section_subsections_edit"),
    path("subsection_details/<int:subsection_id>/", views.subsection_details, name="subsection_details"),
]
