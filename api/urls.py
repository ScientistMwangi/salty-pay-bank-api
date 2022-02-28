from xml.etree.ElementInclude import include
from django.urls import URLPattern, path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('transactiontypes', viewset=views.TransactionTypesViewSet)
router.register('customers', viewset=views.CustomerViewSet)
router.register('accounts', viewset=views.AccountViewSet)
router.register('transfer', viewset=views.TransferViewSet)
app_name = "api"

urlpatterns = [
    path('', include(router.urls)),
    path('customers/<int:id>/accounts',
         views.customer_accounts, name="customer_accounts"),
    path('accounts/<int:id>/history',
         views.account_history_all, name="accounts_details")
]
