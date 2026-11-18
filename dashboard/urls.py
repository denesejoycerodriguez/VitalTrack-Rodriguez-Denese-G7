from django.urls import path
from .views import DashboardRedirectView, NurseDashboardView, AdminDashboardView

urlpatterns = [
    path("", DashboardRedirectView.as_view(), name="dashboard"),
    path("nurse/dashboard/", NurseDashboardView.as_view(), name="nurse_dashboard"),
    path("admin-panel/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]