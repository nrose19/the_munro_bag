import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'munrobag.settings')
django.setup()

from munro_app.forms import ClimbRecordForm
from django.core.files.uploadedfile import SimpleUploadedFile

print("--- Test 1: No data, no files ---")
form = ClimbRecordForm({}, {})
print("Is valid?", form.is_valid())
if not form.is_valid():
    print(form.errors)

print("\n--- Test 2: Data, no files ---")
data = {
    'munro': 1,
    'climb_date': '2026-03-21',
    'total_meters_climbed': 1000,
    'total_distance': 10,
    'time_hr': 2,
    'time_min': 30,
    'star_rating': 5,
    'is_favourite': 'yes',
    'climb_submit': '1'
}
form = ClimbRecordForm(data, {})
print("Is valid?", form.is_valid())
if not form.is_valid():
    print(form.errors)

print("\n--- Test 3: Data, with files ---")
file_data = {'photos': SimpleUploadedFile("test.jpg", b"content")}
form = ClimbRecordForm(data, file_data)
print("Is valid?", form.is_valid())
if not form.is_valid():
    print(form.errors)
