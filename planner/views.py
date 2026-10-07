from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import NoteForm, NoteImageForm, NotePDFForm, StudyItemForm, SubjectForm
from .models import Note, NoteImage, NotePDF, StudyItem, Subject


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


@login_required
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, f"Subject '{subject.name}' added successfully! 📚")
            return redirect("subjects")
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = SubjectForm()

    return render(
        request,
        "planner/add_subject.html",
        {
            "form": form,
        }
    )


@login_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == "POST":
        form = SubjectForm(
            request.POST,
            instance=subject
        )
        if form.is_valid():
            form.save()
            messages.success(request, f"Subject '{subject.name}' updated! ✏️")
            return redirect("subjects")
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = SubjectForm(instance=subject)

    return render(
        request,
        "planner/edit_subject.html",
        {
            "form": form,
            "subject": subject,
        }
    )


@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == "POST":
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject '{name}' deleted! 🗑️")
        return redirect("subjects")

    return render(
        request,
        "planner/delete_subject.html",
        {
            "subject": subject,
        }
    )


@login_required
def subjects(request):
    subjects = Subject.objects.filter(
        user=request.user
    ).annotate(
        study_item_count=Count("study_items"),
        completed_count=Count(
            "study_items",
            filter=Q(study_items__completed=True)
        ),
        pending_count=Count(
            "study_items",
            filter=Q(study_items__completed=False)
        )
    )

    total_study_items = StudyItem.objects.filter(
        subject__user=request.user
    ).count()

    completed_study_items = StudyItem.objects.filter(
        subject__user=request.user,
        completed=True
    ).count()

    pending_study_items = total_study_items - completed_study_items

    if total_study_items > 0:
        overall_progress = int(
            (completed_study_items / total_study_items) * 100
        )
    else:
        overall_progress = 0

    return render(
        request,
        "planner/subjects.html",
        {
            "subjects": subjects,
            "total_study_items": total_study_items,
            "completed_study_items": completed_study_items,
            "pending_study_items": pending_study_items,
            "overall_progress": overall_progress,
        }
    )


@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    study_items = subject.study_items.all().order_by(
        "completed",
        F("due_date").asc(nulls_last=True)
    )

    completed_items = study_items.filter(
        completed=True
    ).count()

    pending_items = study_items.filter(
        completed=False
    ).count()

    total_count = study_items.count()
    if total_count > 0:
        progress = int(
            (completed_items / total_count) * 100
        )
    else:
        progress = 0

    return render(
        request,
        "planner/subject_detail.html",
        {
            "subject": subject,
            "study_items": study_items,
            "completed_items": completed_items,
            "pending_items": pending_items,
            "progress": progress,
        }
    )


@login_required
def add_study_item(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == "POST":
        form = StudyItemForm(request.POST)

        if form.is_valid():
            study_item = form.save(commit=False)
            study_item.subject = subject
            study_item.save()
            messages.success(request, f"Study item '{study_item.title}' created! 📋")
            return redirect(
                "study_item_detail",
                item_id=study_item.id
            )
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = StudyItemForm()

    return render(
        request,
        "planner/add_study_item.html",
        {
            "form": form,
            "subject": subject,
        }
    )


@login_required
def study_item_detail(request, item_id):
    study_item = get_object_or_404(
        StudyItem,
        id=item_id,
        subject__user=request.user
    )

    notes = study_item.notes.all()

    return render(
        request,
        "planner/study_item_detail.html",
        {
            "study_item": study_item,
            "notes": notes,
        }
    )


@login_required
def add_note(request, item_id):
    study_item = get_object_or_404(
        StudyItem,
        id=item_id,
        subject__user=request.user
    )

    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.study_item = study_item
            note.save()
            messages.success(request, "Note added successfully! 📝")
            return redirect(
                "study_item_detail",
                item_id=study_item.id
            )
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = NoteForm()

    return render(
        request,
        "planner/add_note.html",
        {
            "form": form,
            "study_item": study_item,
        }
    )


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        study_item__subject__user=request.user
    )

    if request.method == "POST":
        form = NoteForm(
            request.POST,
            instance=note
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Note updated! ✏️")
            return redirect(
                "study_item_detail",
                item_id=note.study_item.id
            )
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "planner/edit_note.html",
        {
            "form": form,
            "note": note,
        }
    )


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        study_item__subject__user=request.user
    )

    if request.method == "POST":
        item_id = note.study_item.id

        for image in note.images.all():
            if image.image:
                image.image.delete(save=False)

        for pdf in note.pdfs.all():
            if pdf.pdf:
                pdf.pdf.delete(save=False)

        note.delete()
        messages.success(request, "Note deleted! 🗑️")

        return redirect(
            "study_item_detail",
            item_id=item_id
        )

    return redirect(
        "study_item_detail",
        item_id=note.study_item.id
    )


@login_required
def add_note_image(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        study_item__subject__user=request.user
    )

    if request.method == "POST":
        form = NoteImageForm(request.POST, request.FILES)

        if form.is_valid():
            note_image = form.save(commit=False)
            note_image.note = note
            note_image.save()
            messages.success(request, "Image uploaded successfully! 🖼️")
            return redirect(
                "study_item_detail",
                item_id=note.study_item.id
            )
        else:
            messages.error(request, "Failed to upload image. Please check the file.")
    else:
        form = NoteImageForm()

    return render(
        request,
        "planner/add_note_image.html",
        {
            "form": form,
            "note": note,
        }
    )


@login_required
def delete_note_image(request, image_id):
    note_image = get_object_or_404(
        NoteImage,
        id=image_id,
        note__study_item__subject__user=request.user
    )

    if request.method == "POST":
        item_id = note_image.note.study_item.id

        if note_image.image:
            note_image.image.delete(save=False)

        note_image.delete()
        messages.success(request, "Image deleted! 🗑️")

        return redirect(
            "study_item_detail",
            item_id=item_id
        )

    return redirect(
        "study_item_detail",
        item_id=note_image.note.study_item.id
    )


@login_required
def add_note_pdf(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        study_item__subject__user=request.user
    )

    if request.method == "POST":
        form = NotePDFForm(request.POST, request.FILES)

        if form.is_valid():
            note_pdf = form.save(commit=False)
            note_pdf.note = note
            note_pdf.save()
            messages.success(request, "PDF document uploaded successfully! 📄")
            return redirect(
                "study_item_detail",
                item_id=note.study_item.id
            )
        else:
            messages.error(request, "Failed to upload PDF. Please check the file.")
    else:
        form = NotePDFForm()

    return render(
        request,
        "planner/add_note_pdf.html",
        {
            "form": form,
            "note": note,
        }
    )


@login_required
def delete_note_pdf(request, pdf_id):
    note_pdf = get_object_or_404(
        NotePDF,
        id=pdf_id,
        note__study_item__subject__user=request.user
    )

    if request.method == "POST":
        item_id = note_pdf.note.study_item.id

        if note_pdf.pdf:
            note_pdf.pdf.delete(save=False)

        note_pdf.delete()
        messages.success(request, "PDF document deleted! 🗑️")

        return redirect(
            "study_item_detail",
            item_id=item_id
        )

    return redirect(
        "study_item_detail",
        item_id=note_pdf.note.study_item.id
    )


@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)

    study_items = StudyItem.objects.filter(
        subject__user=request.user
    )

    total_items = study_items.count()

    completed_items = study_items.filter(
        completed=True
    ).count()

    pending_items = study_items.filter(
        completed=False
    ).count()

    if total_items > 0:
        progress = int((completed_items / total_items) * 100)
    else:
        progress = 0

    important_items = study_items.filter(
        important=True,
        completed=False
    ).count()

    urgent_items = study_items.filter(
        urgent=True,
        completed=False
    ).count()

    assignment_count = study_items.filter(
        item_type="ASSIGNMENT"
    ).count()

    seminar_count = study_items.filter(
        item_type="SEMINAR"
    ).count()

    other_count = study_items.filter(
        item_type="OTHER"
    ).count()

    alert_count = study_items.filter(
        completed=False
    ).filter(
        Q(important=True) | Q(urgent=True)
    ).count()

    today = timezone.localdate()
    tomorrow = today + timezone.timedelta(days=1)
    week_end = today + timezone.timedelta(days=7)

    upcoming_items = study_items.filter(
        completed=False,
        due_date__gt=week_end
    ).order_by("due_date")[:5]

    today_items = study_items.filter(
        completed=False,
        due_date=today
    )

    overdue_items = study_items.filter(
        completed=False,
        due_date__lt=today
    ).order_by("due_date")

    overdue_count = overdue_items.count()
    due_today_count = today_items.count()

    tomorrow_items = study_items.filter(
        completed=False,
        due_date=tomorrow
    )

    due_tomorrow_count = tomorrow_items.count()

    this_week_items = study_items.filter(
        completed=False,
        due_date__gt=tomorrow,
        due_date__lte=week_end
    ).order_by("due_date")

    return render(
        request,
        "planner/dashboard.html",
        {
            "subjects": subjects,
            "total_items": total_items,
            "completed_items": completed_items,
            "pending_items": pending_items,
            "important_items": important_items,
            "urgent_items": urgent_items,
            "progress": progress,
            "upcoming_items": upcoming_items,
            "alert_count": alert_count,
            "today_items": today_items,
            "due_today_count": due_today_count,
            "tomorrow_items": tomorrow_items,
            "due_tomorrow_count": due_tomorrow_count,
            "this_week_items": this_week_items,
            "overdue_items": overdue_items,
            "overdue_count": overdue_count,
            "assignment_count": assignment_count,
            "seminar_count": seminar_count,
            "other_count": other_count,
        }
    )


@login_required
def alerts(request):
    important_items = StudyItem.objects.filter(
        subject__user=request.user,
        important=True,
        completed=False
    ).order_by("due_date")

    urgent_items = StudyItem.objects.filter(
        subject__user=request.user,
        urgent=True,
        completed=False
    ).order_by("due_date")

    today = timezone.localdate()

    overdue_items = StudyItem.objects.filter(
        subject__user=request.user,
        completed=False,
        due_date__lt=today
    ).order_by("due_date")

    today_items = StudyItem.objects.filter(
        subject__user=request.user,
        completed=False,
        due_date=today
    ).order_by("due_date")

    return render(
        request,
        "planner/alerts.html",
        {
            "important_items": important_items,
            "urgent_items": urgent_items,
            "overdue_items": overdue_items,
            "today_items": today_items,
        }
    )


@login_required
def quick_add(request):
    subjects = Subject.objects.filter(
        user=request.user
    ).order_by("name")

    if request.method == "POST":
        form = StudyItemForm(request.POST)

        if form.is_valid():
            subject_id = request.POST.get("subject")
            subject = get_object_or_404(
                Subject,
                id=subject_id,
                user=request.user
            )

            study_item = form.save(commit=False)
            study_item.subject = subject
            study_item.save()
            messages.success(request, f"Study item '{study_item.title}' added to {subject.name}! 🚀")
            return redirect(
                "study_item_detail",
                item_id=study_item.id
            )
        else:
            messages.error(request, "Please check the form inputs.")
    else:
        form = StudyItemForm()

    return render(
        request,
        "planner/quick_add.html",
        {
            "subjects": subjects,
            "form": form,
        }
    )


@login_required
def toggle_study_item(request, item_id):
    study_item = get_object_or_404(
        StudyItem,
        id=item_id,
        subject__user=request.user
    )

    if request.method == "POST":
        study_item.completed = not study_item.completed
        study_item.save()
        status_str = "completed! 🎉" if study_item.completed else "marked as pending. ⏳"
        messages.success(request, f"Task '{study_item.title}' {status_str}")

    return redirect("study_item_detail", item_id=study_item.id)


@login_required
def delete_study_item(request, item_id):
    study_item = get_object_or_404(
        StudyItem,
        id=item_id,
        subject__user=request.user
    )

    if request.method == "POST":
        subject_id = study_item.subject.id
        title = study_item.title
        study_item.delete()
        messages.success(request, f"Study item '{title}' deleted! 🗑️")

        return redirect(
            "subject_detail",
            subject_id=subject_id
        )

    return redirect(
        "study_item_detail",
        item_id=study_item.id
    )


@login_required
def edit_study_item(request, item_id):
    study_item = get_object_or_404(
        StudyItem,
        id=item_id,
        subject__user=request.user
    )

    if request.method == "POST":
        form = StudyItemForm(request.POST, instance=study_item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Study item '{study_item.title}' updated! ✏️")
            return redirect(
                "study_item_detail",
                item_id=study_item.id
            )
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = StudyItemForm(instance=study_item)

    return render(
        request,
        "planner/edit_study_item.html",
        {
            "form": form,
            "study_item": study_item,
        }
    )