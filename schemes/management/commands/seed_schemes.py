from django.core.management.base import BaseCommand
from schemes.models import Scheme, EligibilityRule, RequiredDocument


class Command(BaseCommand):
    help = "Seed database with realistic government schemes"

    def handle(self, *args, **kwargs):

        self.stdout.write("Seeding schemes...")

        # ---------------- PM KISAN ----------------
        pm_kisan, _ = Scheme.objects.get_or_create(
            name="PM Kisan",
            defaults={
                "description": "Income support scheme for farmers",
                "official_link": "https://pmkisan.gov.in/",
                "category": "Agriculture",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=pm_kisan,
            field_name="occupation",
            operator="eq",
            value="farmer"
        )

        EligibilityRule.objects.get_or_create(
            scheme=pm_kisan,
            field_name="income",
            operator="lte",
            value="200000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_kisan,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_kisan,
            document_name="Land Ownership Proof"
        )


        # ---------------- AYUSHMAN BHARAT ----------------
        ayushman, _ = Scheme.objects.get_or_create(
            name="Ayushman Bharat",
            defaults={
                "description": "Health insurance coverage up to ₹5 lakh per family per year",
                "official_link": "https://beneficiary.nha.gov.in/",
                "category": "Health",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=ayushman,
            field_name="income",
            operator="lte",
            value="300000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=ayushman,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=ayushman,
            document_name="Ration Card"
        )


        # ---------------- PM AWAS YOJANA ----------------
        pm_awas, _ = Scheme.objects.get_or_create(
            name="PM Awas Yojana",
            defaults={
                "description": "Affordable housing scheme for low income families",
                "official_link": "https://pmaymis.gov.in/",
                "category": "Housing",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=pm_awas,
            field_name="income",
            operator="lte",
            value="300000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_awas,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_awas,
            document_name="Income Certificate"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_awas,
            document_name="Residence Proof"
        )


        # ---------------- BETI BACHAO BETI PADHAO ----------------
        beti_bachao, _ = Scheme.objects.get_or_create(
            name="Beti Bachao Beti Padhao",
            defaults={
                "description": "Government initiative to support girl child education and welfare",
                "official_link": "https://wcd.gov.in/women/beti-bachao-beti-padhao",
                "category": "Education",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=beti_bachao,
            field_name="gender",
            operator="eq",
            value="female"
        )

        EligibilityRule.objects.get_or_create(
            scheme=beti_bachao,
            field_name="age",
            operator="lte",
            value="18"
        )

        RequiredDocument.objects.get_or_create(
            scheme=beti_bachao,
            document_name="Birth Certificate"
        )

        RequiredDocument.objects.get_or_create(
            scheme=beti_bachao,
            document_name="Aadhaar Card"
        )


        # ---------------- MUDRA LOAN ----------------
        mudra, _ = Scheme.objects.get_or_create(
            name="Mudra Loan",
            defaults={
                "description": "Loan scheme for small entrepreneurs and businesses",
                "official_link": "https://www.mudra.org.in/",
                "category": "Business",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=mudra,
            field_name="income",
            operator="lte",
            value="500000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=mudra,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=mudra,
            document_name="Bank Passbook"
        )

        RequiredDocument.objects.get_or_create(
            scheme=mudra,
            document_name="Business Plan"
        )


        # ---------------- SKILL INDIA ----------------
        skill_india, _ = Scheme.objects.get_or_create(
            name="Skill India",
            defaults={
                "description": "Skill development program for youth",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=skill_india,
            field_name="age",
            operator="gte",
            value="18"
        )

        EligibilityRule.objects.get_or_create(
            scheme=skill_india,
            field_name="age",
            operator="lte",
            value="45"
        )

        RequiredDocument.objects.get_or_create(
            scheme=skill_india,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=skill_india,
            document_name="Education Certificate"
        )
                # ---------------- PM FASAL BIMA YOJANA ----------------
        pm_fasal, _ = Scheme.objects.get_or_create(
            name="PM Fasal Bima Yojana",
            defaults={
                "description": "Crop insurance scheme for farmers",
                "official_link": "https://pmfby.gov.in/",
                "category": "Agriculture",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=pm_fasal,
            field_name="occupation",
            operator="eq",
            value="farmer"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_fasal,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=pm_fasal,
            document_name="Land Ownership Proof"
        )


        # ---------------- ATAL PENSION YOJANA ----------------
        atal_pension, _ = Scheme.objects.get_or_create(
            name="Atal Pension Yojana",
            defaults={
                "description": "Pension scheme for workers in the unorganized sector",
                "official_link": "https://www.npscra.nsdl.co.in/",
                "category": "Social Security",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=atal_pension,
            field_name="age",
            operator="gte",
            value="18"
        )

        EligibilityRule.objects.get_or_create(
            scheme=atal_pension,
            field_name="age",
            operator="lte",
            value="40"
        )

        RequiredDocument.objects.get_or_create(
            scheme=atal_pension,
            document_name="Aadhaar Card"
        )


        # ---------------- UJJWALA YOJANA ----------------
        ujjwala, _ = Scheme.objects.get_or_create(
            name="PM Ujjwala Yojana",
            defaults={
                "description": "Free LPG connection for women from low-income households",
                "official_link": "https://www.pmuy.gov.in/",
                "category": "Women Welfare",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=ujjwala,
            field_name="gender",
            operator="eq",
            value="female"
        )

        EligibilityRule.objects.get_or_create(
            scheme=ujjwala,
            field_name="income",
            operator="lte",
            value="200000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=ujjwala,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=ujjwala,
            document_name="Ration Card"
        )


        # ---------------- PM SVANIDHI ----------------
        svanidhi, _ = Scheme.objects.get_or_create(
            name="PM SVANidhi",
            defaults={
                "description": "Loan scheme for street vendors",
                "official_link": "https://pmsvanidhi.mohua.gov.in/",
                "category": "Business",
                "is_central": True
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=svanidhi,
            field_name="occupation",
            operator="eq",
            value="street_vendor"
        )

        RequiredDocument.objects.get_or_create(
            scheme=svanidhi,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=svanidhi,
            document_name="Vendor Certificate"
        )


        # ---------------- MAHARASHTRA SCHEMES ----------------

        # Mahatma Jyotiba Phule Jan Arogya Yojana
        mjp, _ = Scheme.objects.get_or_create(
            name="Mahatma Jyotiba Phule Jan Arogya Yojana",
            defaults={
                "description": "Health insurance scheme for Maharashtra residents",
                "official_link": "https://www.jeevandayee.gov.in/",
                "category": "Health",
                "is_central": False
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=mjp,
            field_name="income",
            operator="lte",
            value="100000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=mjp,
            document_name="Aadhaar Card"
        )

        RequiredDocument.objects.get_or_create(
            scheme=mjp,
            document_name="Income Certificate"
        )


        # Shetkari Apghat Vima Yojana
        shetkari_vima, _ = Scheme.objects.get_or_create(
            name="Shetkari Apghat Vima Yojana",
            defaults={
                "description": "Insurance scheme for farmers in Maharashtra",
                "category": "Agriculture",
                "is_central": False
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=shetkari_vima,
            field_name="occupation",
            operator="eq",
            value="farmer"
        )

        RequiredDocument.objects.get_or_create(
            scheme=shetkari_vima,
            document_name="Aadhaar Card"
        )


        # Rajarshi Shahu Maharaj Scholarship
        shahu_scholarship, _ = Scheme.objects.get_or_create(
            name="Rajarshi Shahu Maharaj Scholarship",
            defaults={
                "description": "Scholarship scheme for students in Maharashtra",
                "category": "Education",
                "is_central": False
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=shahu_scholarship,
            field_name="income",
            operator="lte",
            value="800000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=shahu_scholarship,
            document_name="Income Certificate"
        )

        RequiredDocument.objects.get_or_create(
            scheme=shahu_scholarship,
            document_name="Education Certificate"
        )


        # Gharkul Yojana
        gharkul, _ = Scheme.objects.get_or_create(
            name="Pandit Dindayal Upadhyay Gharkul Yojana",
            defaults={
                "description": "Housing scheme for rural poor families in Maharashtra",
                "category": "Housing",
                "is_central": False
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=gharkul,
            field_name="income",
            operator="lte",
            value="200000"
        )

        RequiredDocument.objects.get_or_create(
            scheme=gharkul,
            document_name="Income Certificate"
        )

        RequiredDocument.objects.get_or_create(
            scheme=gharkul,
            document_name="Residence Proof"
        )


        # Krushi Pump Yojana
        krushi_pump, _ = Scheme.objects.get_or_create(
            name="Krushi Pump Yojana",
            defaults={
                "description": "Subsidy scheme for agricultural water pumps",
                "category": "Agriculture",
                "is_central": False
            }
        )

        EligibilityRule.objects.get_or_create(
            scheme=krushi_pump,
            field_name="occupation",
            operator="eq",
            value="farmer"
        )

        RequiredDocument.objects.get_or_create(
            scheme=krushi_pump,
            document_name="Land Ownership Proof"
        )

        self.stdout.write(self.style.SUCCESS("Schemes seeded successfully!"))