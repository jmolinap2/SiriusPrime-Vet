from datetime import datetime

from config import settings
from core.clinic.models import Company
from core.homepage.models import SocialNetworks
from core.security.models import Dashboard


def site_settings(request):
    dashboard = Dashboard.objects.first()
    parameters = {
        'dashboard': dashboard,
        'date_joined': datetime.now(),
        'menu': 'hzt_body.html' if dashboard is None else dashboard.get_template_from_layout(),
        'key_google_maps': settings.KEY_GOOGLE_MAPS,
        'company': Company.objects.first(),
        'social_networks': SocialNetworks.objects.filter(state=True)
    }
    return parameters
