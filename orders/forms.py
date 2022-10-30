from django import forms

from orders.models import Order
class OrderCreateForm(forms.ModelForm):
    regions = ["Greater Accra", "Central","Ahafo","Upper West",
    "Northern","Savannah","North-East","Upper East","Bono East","Brong Ahafo",
    "Oti","Volta","Eastern","Western","Western North","Ashanti"]
    choices = [(i, str(i)) for i in regions]
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-input form"}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={"class":"form-input form"}))
    region = forms.ChoiceField(choices=sorted(choices),
    widget=forms.Select(attrs={"class":"form-control"}))

    class Meta:
        model = Order
        fields = ["address","postal_code","region"]
