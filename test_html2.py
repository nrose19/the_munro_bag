import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'munrobag.settings')
django.setup()

from munro_app.forms import ClimbRecordForm
form = ClimbRecordForm()
for radio in form['is_favourite']:
    print(radio.tag())
