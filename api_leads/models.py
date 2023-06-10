from django.db import models


class Lead(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    referral_source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead {self.id}"
