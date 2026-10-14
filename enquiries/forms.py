from django import forms

from .models import EnquiryKind


class EnquiryForm(forms.Form):
    kind = forms.ChoiceField(choices=EnquiryKind.choices, widget=forms.HiddenInput)
    full_name = forms.CharField(max_length=160, label="Your name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=32, required=False)
    organisation = forms.CharField(max_length=180, required=False)
    job_title = forms.CharField(max_length=120, required=False)
    employee_count = forms.IntegerField(min_value=1, required=False)
    licence_reference = forms.CharField(max_length=120, required=False)
    subject = forms.CharField(max_length=180, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), max_length=3000)
    consent_to_contact = forms.BooleanField(label="I agree that the team may contact me about this request.")
    marketing_opt_in = forms.BooleanField(required=False, label="Send me occasional company and product updates.")
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kind = self.initial.get('kind') or self.data.get('kind')
        if kind != EnquiryKind.EMPLOYER:
            self.fields.pop('employee_count')
        if kind != EnquiryKind.PROVIDER:
            self.fields.pop('licence_reference')
        if kind in {EnquiryKind.EMPLOYER, EnquiryKind.PROVIDER, EnquiryKind.DEMO}:
            self.fields['organisation'].required = True
            self.fields['organisation'].error_messages['required'] = 'Enter your organisation name.'
        if kind == EnquiryKind.EMPLOYER:
            self.fields['employee_count'].required = True
            self.fields['employee_count'].error_messages['required'] = 'Enter an approximate employee count.'
        if kind == EnquiryKind.PROVIDER:
            self.fields['licence_reference'].required = True
            self.fields['licence_reference'].error_messages['required'] = 'Enter the institution licence or registration reference.'
        for name, token in {'full_name': 'name', 'email': 'email', 'phone': 'tel',
                            'organisation': 'organization', 'job_title': 'organization-title'}.items():
            self.fields[name].widget.attrs['autocomplete'] = token

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Unable to submit this request.")
        return ""

FIELD_PLACEHOLDERS = {
    "full_name": "e.g. Thandiwe Phiri",
    "email": "e.g. name@gmail.com",
    "phone": "+265 …",
    "organisation": "Organisation name",
    "job_title": "Your role",
    "employee_count": "Approximate workforce",
    "licence_reference": "Licence or registration reference",
    "subject": "A short summary",
    "message": "Tell us what you need, without including passwords, full identity numbers or payroll files.",
}


def style_form(form):
    for name, field in form.fields.items():
        if not isinstance(field.widget, (forms.HiddenInput, forms.CheckboxInput)):
            field.widget.attrs["class"] = "field__control"
            field.widget.attrs["placeholder"] = FIELD_PLACEHOLDERS.get(name, "")
    return form
