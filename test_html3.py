import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'munrobag.settings')
django.setup()

from munro_app.forms import ClimbRecordForm
form = ClimbRecordForm()
print(form['time_hr'].as_widget())
print(form['time_min'].as_widget())
