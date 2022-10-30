from django import forms
from authentications.models import Users
class LoginForm(forms.Form):
    """Creating the actual form field view"""
    email_address = forms.CharField(max_length=50, required=True,
    widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(max_length=50,
    widget=forms.PasswordInput(attrs={"class":"form-control"}))

class UserRegistrationForm(forms.ModelForm):
    """User registration model form"""
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email_address = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={"class":"form-control"}),
    label="Password")
    password2 = forms.CharField(label="Confirm Password",
    widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        """Already contained in form"""
        model = Users
        fields = ["first_name", "last_name","email_address","phone_number"]

    def clean_password2(self):
        """Checking if passwords matches"""
        clean_data = self.cleaned_data
        if clean_data["password"]!=clean_data["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return clean_data["password2"]


class UserForgetPassword(forms.Form):
    """Forgot password form"""
    email_address = forms.CharField(max_length=50, required=True,
    widget=forms.EmailInput(attrs={"class":"form-control"}))

class UserForgetPasswordConfirm(forms.Form):
    """Forgot password form"""
    new_password = forms.CharField(max_length=50, required=True,
    widget=forms.PasswordInput(attrs={"class":"form-control"}))
    confim_password = forms.CharField(max_length=50, required=True,
    widget=forms.PasswordInput(attrs={"class":"form-control"}))

    def clean(self):
        cd = self.cleaned_data
        new_password = cd.get("new_password")
        confim_password = cd.get("confim_password")
        if new_password != confim_password:
            raise forms.ValidationError("Password did not match")
        else:
            return cd
