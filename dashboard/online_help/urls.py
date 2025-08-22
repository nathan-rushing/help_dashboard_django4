from django.urls import path
from . import views

app_name = 'online_help'

urlpatterns = [
    path("home_test/", views.home_test, name="home_test"),
    path("tasks_test/", views.tasks_test, name="tasks_test"),
    path("document_list/", views.document_list, name="document_list"),
    path("documents_list_edit/edit/", views.document_list_edit, name="document_list_edit"),
    path("documents/<int:pk>/rename/", views.document_rename, name="document_rename"),
    path("documents/<int:pk>/remove/", views.document_remove, name="document_remove"),
    path("documents_sections/<int:document_id>/", views.document_sections, name="document_sections"),
    path("documents_section_edit/<int:document_id>/sections/edit/", views.document_sections_edit, name="document_sections_edit"),
    path("sections/<int:section_id>/rename/", views.section_rename, name="section_rename"),
    path("sections/<int:section_id>/delete/", views.section_delete, name="section_delete"),
    path("section_subsections/<int:section_id>/", views.section_subsections, name="section_subsections"),
    path("section_subsections_edit/<int:section_id>/subsections/edit/", views.section_subsections_edit, name="section_subsections_edit"),
    path("subsection/<int:subsection_id>/rename/", views.subsection_rename, name="subsection_rename"),
    path("subsection_details/<int:subsection_id>/", views.subsection_details, name="subsection_details"),
    path("sme/<int:pk>/edit/", views.edit_sme, name="edit_sme"),
    path("edit_sme/<int:sme_id>/", views.edit_sme, name="edit_sme"),
    path("add_sme/<int:subsection_id>/", views.add_sme, name="add_sme"),
    path("assign_task/", views.assign_task, name="assign_task"),
    # AJAX endpoints for assign_task
    path('ajax/load-sections/', views.load_sections, name='ajax_load_sections'),
    path('ajax/load-subsections/', views.load_subsections, name='ajax_load_subsections'),
]
