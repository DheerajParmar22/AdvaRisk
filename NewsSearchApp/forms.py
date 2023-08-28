# Django's built-in form handling and validation

from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=True)
