from django.contrib import admin
from .models import Subject, StudyItem, Note, NoteImage, NotePDF


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "semester", "user", "created_at")
    list_filter = ("semester",)
    search_fields = ("name", "code")


@admin.register(StudyItem)
class StudyItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "item_type",
        "priority",
        "due_date",
        "completed",
    )

    list_filter = (
        "item_type",
        "priority",
        "completed",
    )

    search_fields = (
        "title",
        "description",
    )

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "study_item",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "content",
    )


@admin.register(NoteImage)
class NoteImageAdmin(admin.ModelAdmin):
    list_display = (
        "note",
        "caption",
        "uploaded_at",
    )

    search_fields = (
        "caption",
        "note__title",
    )


@admin.register(NotePDF)
class NotePDFAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "note",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "note__title",
    )