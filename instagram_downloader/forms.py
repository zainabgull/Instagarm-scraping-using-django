# forms.py
from django import forms

class InstagramScrapeForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    hashtag = forms.CharField(max_length=100, label='Hashtag')
