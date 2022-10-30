from django import forms

from shop.models import Product, Category
class ProductCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label ="Select",
    widget=forms.Select(attrs={"class":"form-control"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-input form"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class":"form-input form"}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={"class":"form-input form"}))

    class Meta:
        model = Product
        fields = ["category","name","description","image","price"]

class SearchForm(forms.Form):
    """Creating the search form class"""
    query = forms.CharField(label="")


class ContactUs(forms.Form):
    """Creating the form for contact us page"""
    name = forms.CharField()
    subject = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 85}), max_length=160)
    phone = forms.CharField()
    field_order = ["name","subject","email","phone","message"]
