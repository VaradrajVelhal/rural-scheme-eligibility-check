from django.shortcuts import render, redirect, get_object_or_404
from .forms import EligibilityForm, RegisterForm
from .services.eligibility_engine import evaluate_schemes
from django.contrib.auth.decorators import login_required
from .models import EligibilityCheck, Scheme
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import login


# -------------------------------
# Landing Page
# -------------------------------

def home(request):
    return render(request, "landing.html")


# -------------------------------
# Eligibility Form
# -------------------------------

@login_required
def check_scheme(request):

    results = None
    eligible_count = 0
    not_eligible_count = 0

    if request.method == "POST":

        form = EligibilityForm(request.POST)

        if form.is_valid():

            user_data = form.cleaned_data
            results = sorted(
                evaluate_schemes(user_data),
                key=lambda x: not x["is_eligible"]
            )

            eligible_count = sum(1 for r in results if r["is_eligible"])
            not_eligible_count = len(results) - eligible_count

            for result in results:
                EligibilityCheck.objects.update_or_create(
                    user=request.user,
                    scheme=result["scheme"],
                    defaults={"is_eligible": result["is_eligible"]}
                )

    else:
        form = EligibilityForm()

    return render(request, "schemes/check.html", {
        "form": form,
        "results": results,
        "eligible_count": eligible_count,
        "not_eligible_count": not_eligible_count,
    })


# -------------------------------
# User Dashboard
# -------------------------------

@login_required
def dashboard(request):

    checks = EligibilityCheck.objects.filter(
        user=request.user
    ).order_by("-checked_at")

    return render(request, "schemes/dashboard.html", {
        "checks": checks
    })


# -------------------------------
# Download PDF Report
# -------------------------------

@login_required
def download_report(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="eligibility_report.pdf"'

    document_template = SimpleDocTemplate(response, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Rural Government Scheme Eligibility Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>User:</b> {request.user.username}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Generated on:</b> {now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Scheme Evaluation Details", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    checks = EligibilityCheck.objects.filter(user=request.user).select_related("scheme")

    for check in checks:

        scheme = check.scheme
        status = "Eligible" if check.is_eligible else "Not Eligible"

        elements.append(Paragraph(f"<b>Scheme:</b> {scheme.name}", styles["Heading3"]))
        elements.append(Paragraph(f"<b>Status:</b> {status}", styles["Normal"]))
        elements.append(Spacer(1, 6))

        if scheme.description:
            elements.append(Paragraph(f"<b>Description:</b> {scheme.description}", styles["Normal"]))
            elements.append(Spacer(1, 6))

        if hasattr(scheme, "official_link") and scheme.official_link:
            elements.append(
                Paragraph(f"<b>Official Website:</b> {scheme.official_link}", styles["Normal"])
            )
            elements.append(Spacer(1, 6))

        if check.is_eligible:
            required_docs = scheme.requireddocument_set.all()

            if required_docs.exists():
                elements.append(Paragraph("<b>Required Documents:</b>", styles["Normal"]))

                for doc in required_docs:
                    elements.append(
                        Paragraph(f"• {doc.document_name}", styles["Normal"])
                    )

        elements.append(Spacer(1, 14))

    document_template.build(elements)

    return response


# -------------------------------
# Analytics Dashboard
# -------------------------------

@login_required
def analytics_dashboard(request):

    total_users = User.objects.count()
    total_checks = EligibilityCheck.objects.count()

    scheme_stats = (
        EligibilityCheck.objects
        .values("scheme__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    eligible_count = EligibilityCheck.objects.filter(is_eligible=True).count()
    not_eligible_count = EligibilityCheck.objects.filter(is_eligible=False).count()

    context = {
        "total_users": total_users,
        "total_checks": total_checks,
        "scheme_stats": scheme_stats,
        "eligible_count": eligible_count,
        "not_eligible_count": not_eligible_count,
    }

    return render(request, "schemes/analytics.html", context)


# -------------------------------
# User Registration
# -------------------------------

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("check_scheme")

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {
        "form": form
    })


# -------------------------------
# Scheme Detail Page
# -------------------------------

def scheme_detail(request, scheme_id):

    scheme = get_object_or_404(Scheme, pk=scheme_id)
    rules = scheme.eligibilityrule_set.all()
    documents = scheme.requireddocument_set.all()

    context = {
        "scheme": scheme,
        "rules": rules,
        "documents": documents
    }

    return render(request, "schemes/scheme_detail.html", context)