from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone

student = get_user_model()

class Leave(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    scanned_count = models.IntegerField(default=0)
    first_scan_time = models.DateTimeField(null=True, blank=True)
    last_scan_time = models.DateTimeField(null=True, blank=True)

    def leaves_per_month(self):
        if self.last_scan_time:
            month = self.last_scan_time.month
            year = self.last_scan_time.year
            return Leave.objects.filter(
                user=self.user,
                last_scan_time__month=month,
                last_scan_time__year=year
            ).count()
        return 0

class Outing(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE)
    out_date = models.DateField()
    out_time = models.TimeField(null=True, blank=True)
    in_time = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    scanned_count = models.IntegerField(default=0)
    first_scan_time = models.DateTimeField(null=True, blank=True)
    last_scan_time = models.DateTimeField(null=True, blank=True)

    def outings_per_month(self):
        if self.last_scan_time:
            month = self.last_scan_time.month
            year = self.last_scan_time.year
            return Outing.objects.filter(
                user=self.user,
                last_scan_time__month=month,
                last_scan_time__year=year
            ).count()
        return 0
