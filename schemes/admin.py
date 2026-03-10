from django.contrib import admin
from .models import State, Scheme, EligibilityRule, RequiredDocument
from .models import EligibilityCheck

admin.site.register(State)
admin.site.register(Scheme)
admin.site.register(EligibilityRule)
admin.site.register(RequiredDocument)
admin.site.register(EligibilityCheck)