import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'munrobag.settings')
django.setup()

from munro_app.models import ClimbRecord, Munro
from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.first()
m = Munro.objects.first()

c = ClimbRecord(
    user=u,
    munro=m,
    climb_date='2026-03-15',
    total_meters_climbed=1000,
    total_distance=10,
    completion_time_hours=2.5,
    star_rating=5
)
try:
    c.save()
    print("Saved successfully with completion_time_hours=", c.completion_time_hours)
except Exception as e:
    print("Error saving:", e)
