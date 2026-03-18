import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'munrobag.settings')
django.setup()

from munro_app.forms import ClimbRecordForm
from munro_app.models import Munro

m = Munro.objects.first()

data = {
    'munro': m.id if m else 1,
    'climb_date': '2026-03-15',
    'total_meters_climbed': 1000,
    'total_distance': '10.5',
    'time_hr': 2,
    'time_min': 30,
    'star_rating': 5,
    'is_favourite': 'yes',
    'climb_submit': '1'
}

form = ClimbRecordForm(data)
print("Is valid with float distance?", form.is_valid())
if not form.is_valid():
    print(form.errors)
