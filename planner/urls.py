from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("alerts/", views.alerts, name="alerts"),

    path("quick-add/", views.quick_add, name="quick_add"),

    path("subjects/", views.subjects, name="subjects"),
    path("subjects/add/", views.add_subject, name="add_subject"),
    path("subjects/<int:subject_id>/", views.subject_detail, name="subject_detail"),
    path("subjects/<int:subject_id>/add/", views.add_study_item, name="add_study_item"),
    path("subjects/<int:subject_id>/edit/", views.edit_subject, name="edit_subject"),
    path("subjects/<int:subject_id>/delete/", views.delete_subject, name="delete_subject"),

    path("study-item/<int:item_id>/", views.study_item_detail, name="study_item_detail"),
    path("study-item/<int:item_id>/add-note/", views.add_note, name="add_note"),
    path("study-item/<int:item_id>/edit/", views.edit_study_item, name="edit_study_item"),
    path("study-item/<int:item_id>/toggle/", views.toggle_study_item, name="toggle_study_item"),
    path("study-item/<int:item_id>/delete/", views.delete_study_item, name="delete_study_item"),

    path("note/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("note/<int:note_id>/delete/", views.delete_note, name="delete_note"),
    path("note/<int:note_id>/add-image/", views.add_note_image, name="add_note_image"),
    path("note-image/<int:image_id>/delete/", views.delete_note_image, name="delete_note_image"),
    path("note/<int:note_id>/add-pdf/", views.add_note_pdf, name="add_note_pdf"),
    path("note-pdf/<int:pdf_id>/delete/", views.delete_note_pdf, name="delete_note_pdf"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]