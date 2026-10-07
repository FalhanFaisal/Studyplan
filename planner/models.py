from django.conf import settings
from django.db import models


class Subject(models.Model):

    SEMESTER_CHOICES = [
        ("FIRST", "First Semester"),
        ("SECOND", "Second Semester"),
        ("THIRD", "Third Semester"),
        ("FOURTH", "Fourth Semester"),
        ("FIFTH", "Fifth Semester"),
        ("SIXTH", "Sixth Semester"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, blank=True)
    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StudyItem(models.Model):

    ITEM_TYPE_CHOICES = [
        ("STUDY", "Study Topic"),
        ("ASSIGNMENT", "Assignment"),
        ("SEMINAR", "Seminar"),
        ("LAB", "Lab"),
        ("PROJECT", "Project"),
        ("OTHER", "Other Work"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="study_items"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES,
        default="STUDY"
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="MEDIUM"
    )

    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    important = models.BooleanField(default=False)

    urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Note(models.Model):

    study_item = models.ForeignKey(
        StudyItem,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    title = models.CharField(max_length=200)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NoteImage(models.Model):

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="notes/")
    caption = models.CharField(max_length=200, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Image for {self.note.title}"


class NotePDF(models.Model):

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    pdf = models.FileField(upload_to="notes/pdfs/")
    title = models.CharField(max_length=200, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.pdf.name