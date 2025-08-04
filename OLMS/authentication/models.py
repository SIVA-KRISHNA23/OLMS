from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICE = [
    ('warden', "Warden"),
    ('security', "Security"),
    ('student', "Student")
]

HOSTEL_CHOICES = [
    ('I1', 'I1'),
    ('I2', 'I2')
]

class CustomUser(AbstractUser):
    email = models.EmailField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICE)
    hostel = models.CharField(max_length=2, choices=HOSTEL_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to='student_images/', null=True, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Ensure that hostel choice is only set for wardens
        if self.role != 'warden':
            self.hostel = None
        super().save(*args, **kwargs)
