from argparse import Namespace
from django.urls import path, include
from .views import DashboardView, AddDomainsView, VerifyDomainView, DeleteDomainsView

app_name = "domains"

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('add-domain', AddDomainsView.as_view(), name="add-domain"),
    path('delete-domain', DeleteDomainsView.as_view(), name="delete-domain"),
    path('verify-domain', VerifyDomainView.as_view(), name="verify-domain"),
]