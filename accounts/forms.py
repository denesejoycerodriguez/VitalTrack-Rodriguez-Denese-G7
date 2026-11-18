from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser

MAX_UPLOAD = 5 * 1024 * 1024  


class StyledFormMixin:
    """Adds Bootstrap classes and error state to every widget."""

    def _style(self):
        for name, field in self.fields.items():
            widget = field.widget
            css = "form-control"
            if isinstance(widget, forms.CheckboxInput):
                css = "form-check-input"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css}".strip()
            if self.is_bound and name in self.errors:
                widget.attrs["class"] += " is-invalid"


class EmailCleanMixin:
    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        taken = CustomUser.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            taken = taken.exclude(pk=self.instance.pk)
        if taken.exists():
            raise forms.ValidationError("An account with this email already exists.")  # BR-14
        return email


class LoginForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(
        label="Username or email",
        widget=forms.TextInput(attrs={"autofocus": True, "autocomplete": "username"}),
    )
    error_messages = {
        "invalid_login": "That username/email and password don't match. Check both and try again.",
        "inactive": "This account is inactive. Ask an administrator to reactivate it.",  # BR-15
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class CustomUserCreationForm(StyledFormMixin, EmailCleanMixin, UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("first_name", "last_name", "username", "email", "contact_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autocomplete"] = "given-name"
        self.fields["last_name"].widget.attrs["autocomplete"] = "family-name"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["contact_number"].widget.attrs["autocomplete"] = "tel"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].label = "Confirm password"
        self._style()


class ProfileUpdateForm(StyledFormMixin, EmailCleanMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "contact_number", "profile_photo")
        widgets = {"profile_photo": forms.FileInput(attrs={"accept": "image/*"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_profile_photo(self):
        photo = self.cleaned_data.get("profile_photo")
        if photo and hasattr(photo, "size") and photo.size > MAX_UPLOAD:  
            raise forms.ValidationError("Profile photo must not exceed 5MB.")
        return photo