mport os
import sys

# setup PYTHONPATH and env vars for apache
sys.path.append('/home/esalazar/iap_web/edex')
os.environ['DJANGO_SETTINGS_MODULE'] = 'edex.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
