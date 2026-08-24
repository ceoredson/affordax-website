from django.urls import path

from . import views

app_name = "enquiries"

urlpatterns = [
    path("thanks/", views.thanks, name="thanks"),
    path("<str:page_name>/", views.enquiry_page, name="form"),
]

