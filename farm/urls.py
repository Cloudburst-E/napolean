from django.urls import path

from .views import DeletePhoneView, PhoneActionView, ProviderIndexView, ProviderPhonesView, ScriptStatusView

urlpatterns = [
    path("providers/", ProviderIndexView.as_view(), name="provider-index"),
    path("providers/<str:provider_name>/phones", ProviderPhonesView.as_view(), name="provider-phones"),
    path(
        "providers/<str:provider_name>/phones/<str:phone_id>/<str:action>",
        PhoneActionView.as_view(),
        name="phone-action",
    ),
    path(
        "providers/<str:provider_name>/phones/<str:phone_id>/script",
        ScriptStatusView.as_view(),
        name="script-status",
    ),
    path("providers/<str:provider_name>/phones/<str:phone_id>", DeletePhoneView.as_view(), name="phone-delete"),
]
