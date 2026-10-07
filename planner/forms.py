from django import forms

from .models import Subject, StudyItem, Note, NoteImage, NotePDF


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "name",
            "code",
            "semester",
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }


class StudyItemForm(forms.ModelForm):

    class Meta:
        model = StudyItem

        fields = [
            "title",
            "item_type",
            "priority",
            "due_date",
            "description",
            "completed",
            "important",
            "urgent",
        ]

        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note

        fields = [
            "title",
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 8}
            ),
        }


class NoteImageForm(forms.ModelForm):

    class Meta:
        model = NoteImage

        fields = [
            "image",
        ]


class NotePDFForm(forms.ModelForm):

    class Meta:
        model = NotePDF

        fields = [
            "pdf",
        ]