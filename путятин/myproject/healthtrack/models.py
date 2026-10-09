from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Личные диапазоны (цели)
    target_systolic_min = models.PositiveIntegerField(default=110)
    target_systolic_max = models.PositiveIntegerField(default=130)
    target_diastolic_min = models.PositiveIntegerField(default=70)
    target_diastolic_max = models.PositiveIntegerField(default=85)
    target_pulse_min = models.PositiveIntegerField(default=60)
    target_pulse_max = models.PositiveIntegerField(default=90)

    def __str__(self):
        return f'Профиль {self.user.username}'

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurements')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    systolic = models.PositiveIntegerField(verbose_name="Систолическое (верхнее)")
    diastolic = models.PositiveIntegerField(verbose_name="Диастолическое (нижнее)")
    pulse = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.systolic}/{self.diastolic} от {self.timestamp.strftime('%d.%m %H:%M')}"

    @property
    def is_normal(self):
        profile = self.user.profile
        systolic_ok = profile.target_systolic_min <= self.systolic <= profile.target_systolic_max
        diastolic_ok = profile.target_diastolic_min <= self.diastolic <= profile.target_diastolic_max
        pulse_ok = profile.target_pulse_min <= self.pulse <= profile.target_pulse_max
        return systolic_ok and diastolic_ok and pulse_ok