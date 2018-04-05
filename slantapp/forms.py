from django import forms
from django.forms import ModelForm

class ContactForm(forms.Form):
  name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))