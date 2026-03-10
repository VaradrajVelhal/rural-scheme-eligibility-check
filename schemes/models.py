from django.db import models
from django.contrib.auth.models import User
class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Scheme(models.Model):

    name = models.CharField(max_length=255)

    description = models.TextField()

    official_link = models.URLField(blank=True, null=True)

    deadline = models.DateField(blank=True, null=True)

    category = models.CharField(max_length=100, blank=True)

    is_central = models.BooleanField(default=True)

    states = models.ManyToManyField("State", blank=True)

    def __str__(self):
        return self.name


class EligibilityRule(models.Model):
    OPERATORS = [
        ('lt', 'Less Than'),
        ('gt', 'Greater Than'),
        ('eq', 'Equal'),
        ('lte', 'Less Than Equal'),
        ('gte', 'Greater Than Equal'),
        ("in", "In List"),
    ]

    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    operator = models.CharField(max_length=10, choices=OPERATORS)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.scheme.name} - {self.field_name}"


class RequiredDocument(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=200)

    def __str__(self):
        return self.document_name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    income = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    land_ownership = models.CharField(max_length=10, blank=True)
    disability_status = models.CharField(max_length=10, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    
class EligibilityCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)
    is_eligible = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'scheme')