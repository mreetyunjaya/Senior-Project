from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models


class Vuln(models.Model):
    cve = models.CharField(max_length=10)
    title = models.CharField(max_length=120)
    risk_score = models.IntegerField(default=1)
    summary = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("vuln-detail", kwargs={"pk": self.pk})


class Remedy(models.Model):
    remediation = models.TextField()
    status = models.CharField(max_length=60, null=True)
    patches = models.CharField(max_length=200)
    approved_remedy = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vulnerability = models.ForeignKey(Vuln, on_delete=models.CASCADE, related_name="rems")

    def __str__(self):
        return self.remediation

    def approve(self):
        self.approved_remedy = True
        self.save()
