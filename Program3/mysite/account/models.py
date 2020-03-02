from django.db import models


class UserAccount(models.Model):
    user_email = models.CharField(max_length=50, primary_key=True)
    user_name = models.CharField(max_length=15)
    user_password = models.CharField(max_length=30)

    def __str__(self):
        return self.user_email
