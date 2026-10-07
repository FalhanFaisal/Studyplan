from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from planner.models import Note, StudyItem, Subject

User = get_user_model()


class StudyPlanTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="student@example.com",
            password="Password123!"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="Password123!"
        )

        self.subject = Subject.objects.create(
            user=self.user,
            name="Computer Science 101",
            code="CS101",
            semester="FIRST",
            description="Intro to Programming"
        )

        self.study_item = StudyItem.objects.create(
            subject=self.subject,
            title="Python Functions Lab",
            item_type="LAB",
            priority="HIGH",
            important=True,
            urgent=False
        )

        self.note = Note.objects.create(
            study_item=self.study_item,
            title="Functions Cheatsheet",
            content="def function_name(args): return True"
        )

    def test_home_redirect(self):
        # Unauthenticated user visiting / redirects to login
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_signup_view(self):
        response = self.client.post(reverse("signup"), {
            "email": "newstudent@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="newstudent@example.com").exists())

    def test_dashboard_login_required(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_access_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Computer Science 101")

    def test_subject_multi_tenant_isolation(self):
        # other_user cannot access user's subject detail
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("subject_detail", args=[self.subject.id]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_study_item(self):
        self.client.force_login(self.user)
        self.assertFalse(self.study_item.completed)
        response = self.client.post(reverse("toggle_study_item", args=[self.study_item.id]))
        self.assertEqual(response.status_code, 302)
        self.study_item.refresh_from_db()
        self.assertTrue(self.study_item.completed)
