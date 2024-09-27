from django.urls import path
from .views.client_report.views import ClientReportView
from .views.earnings_report.views import EarningsReportView
from .views.purchase_report.views import PurchaseReportView
from .views.sale_report.views import SaleReportView
from .views.mascot_report.views import MascotReportView

urlpatterns = [
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('client/', ClientReportView.as_view(), name='client_report'),
    path('mascot/', MascotReportView.as_view(), name='mascot_report'),
    path('earnings/', EarningsReportView.as_view(), name='earnings_report'),
]
