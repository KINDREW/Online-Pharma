"""Forms.py"""
from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Adding product to cart"""
    quantity =quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        widget=forms.Select(attrs ={"class":"form-control quantity"}))
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
