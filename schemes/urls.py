from django.urls import path
from .views import analytics_dashboard, check_scheme, dashboard, download_report, register, scheme_detail, home

urlpatterns = [
    path("", home, name="home"),   # landing page

    path("check/", check_scheme, name="check_scheme"),  # eligibility form

    path("dashboard/", dashboard, name="dashboard"),
    path("download-report/", download_report, name="download_report"),
    path("analytics/", analytics_dashboard, name="analytics_dashboard"),
    path("register/", register, name="register"),
    path("scheme/<int:scheme_id>/", scheme_detail, name="scheme_detail"),
]