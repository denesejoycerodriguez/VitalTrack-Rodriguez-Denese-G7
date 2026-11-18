from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.models import CustomUser


class DashboardRedirectView(LoginRequiredMixin, View):
    """Sends each user to the dashboard for their role."""

    def get(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.ADMIN:
            return redirect("admin_dashboard")
        return redirect("nurse_dashboard")


class NurseDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/nurse_dashboard.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.NURSE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modules"] = [
            {"icon": "S", "title": "Student profiles", "text": "Create and update health profiles, conditions, and allergies."},
            {"icon": "M", "title": "Medication log", "text": "Record each dose with amount, time, and who gave it."},
            {"icon": "V", "title": "Clinic visits", "text": "Log symptoms and treatment for every visit."},
            {"icon": "I", "title": "Immunizations", "text": "Track vaccines and see who is due."},
        ]
        return context


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/admin_dashboard.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.ADMIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = CustomUser.objects
        context["total_users"] = users.count()
        context["nurse_count"] = users.filter(role=CustomUser.Role.NURSE).count()
        context["admin_count"] = users.filter(role=CustomUser.Role.ADMIN).count()
        context["inactive_count"] = users.filter(is_active=False).count()
        context["recent_users"] = users.order_by("-date_joined")[:6]
        return context