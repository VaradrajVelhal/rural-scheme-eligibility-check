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
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_staff or user.is_superuser




def no_cache(view_func):
    decorated_view_func = never_cache(view_func)
    return decorated_view_func
# -------------------------------
# Custom logout Page
# -------------------------------

@never_cache
def custom_logout(request):
    logout(request)
    response = redirect('home')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# -------------------------------
# Landing Page
# -------------------------------

def home(request):
    return render(request, "landing.html")


# -------------------------------
# Eligibility Form
# -------------------------------

@never_cache
@login_required(login_url='login')
def check_scheme(request):

    if request.method == "POST":
        form = EligibilityForm(request.POST)

        if form.is_valid():
            user_data = form.cleaned_data

            results = sorted(
                evaluate_schemes(user_data),
                key=lambda x: not x["is_eligible"]
            )

            # Save in session
            serialized_results = []

            for r in results:
                serialized_results.append({
                 "scheme_id": r["scheme"].id,
                "scheme_name": r["scheme"].name,
                "description": r["scheme"].description,
                 "is_eligible": r["is_eligible"],
                "rules": r["rules"]
                })

            request.session["results"] = serialized_results
            safe_form_data = user_data.copy()

            # Convert state object to string or id
            if safe_form_data.get("state"):
                safe_form_data["state"] = safe_form_data["state"].name   # or .id

            request.session["form_data"] = safe_form_data

            # Save history (your existing logic)
            for result in results:
                EligibilityCheck.objects.create(
                    user=request.user,
                    scheme=result["scheme"],
                    is_eligible=result["is_eligible"]
                )
                print(f"DEBUG: Saved EligibilityCheck for {result['scheme'].name}")

            return redirect("check_scheme")   # IMPORTANT

    else:
        # GET request → load from session
        form_data = request.session.get("form_data")
        results = request.session.get("results", [])

        if form_data:
            if form_data and form_data.get("state"):
                from .models import State
            try:
                form_data["state"] = State.objects.get(name=form_data["state"])
            except:
             pass

            form = EligibilityForm(initial=form_data)
        else:
            form = EligibilityForm()

    # Handle counts safely
    if results:
        eligible_count = sum(1 for r in results if r["is_eligible"])
        not_eligible_count = len(results) - eligible_count
        show_results = True
    else:
        eligible_count = 0
        not_eligible_count = 0
        show_results = False

    return render(request, "schemes/check.html", {
        "form": form,
        "results": results,
        "eligible_count": eligible_count,
        "not_eligible_count": not_eligible_count,
        "show_results": show_results,
    })

# -------------------------------
# User Dashboard
# -------------------------------

@never_cache
@login_required(login_url='login')
def dashboard(request):

    checks = EligibilityCheck.objects.filter(user=request.user).order_by('-checked_on')

    return render(request, "schemes/dashboard.html", {
        "checks": checks
    })


# -------------------------------
# Download PDF Report
# -------------------------------

@never_cache
@login_required(login_url='login')
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

@never_cache
@user_passes_test(is_admin, login_url='dashboard')
@login_required(login_url='login')
def analytics_dashboard(request):

    total_users = User.objects.count()
    total_checks = EligibilityCheck.objects.count()

    scheme_stats = (
        EligibilityCheck.objects
        .values("scheme__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
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

    # Get eligibility status from session if possible
    is_eligible = None
    session_results = request.session.get("results", [])
    for r in session_results:
        if isinstance(r, dict) and r.get("scheme_id") == scheme_id:
            is_eligible = r.get("is_eligible")
            break

    context = {
        "scheme": scheme,
        "rules": rules,
        "documents": documents,
        "is_eligible": is_eligible
    }

    return render(request, "schemes/scheme_detail.html", context)

def set_language(request):
    lang = request.GET.get("lang", "en")

    if lang not in ["en", "mr", "hi"]:
        lang = "en"

    request.session["lang"] = lang
    return redirect(request.META.get("HTTP_REFERER", "/"))