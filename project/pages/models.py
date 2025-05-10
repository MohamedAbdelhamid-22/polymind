from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    points = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)

    def set_password(self, raw_password):
        """Hash the password before saving."""
        if raw_password and not raw_password.startswith("pbkdf2_"):  # Avoid double hashing
            self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check the provided password against the stored hash."""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Only hash the password if it's not already hashed
        if not self.password.startswith("pbkdf2_"):  
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
  

class Challenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    expected_result = models.FloatField()
    points = models.IntegerField(default=0)
    end_time = models.DateTimeField(default=None, null=True, blank=True)
    is_ended = models.BooleanField(default=False)


    def __str__(self):
        return self.title

class ChallengeResult(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE)
    accuracy = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'challenge'], name='unique_user_challenge')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.accuracy}%)"