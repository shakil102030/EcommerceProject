from django import forms

class BlogSearchForm(forms.Form):
	q = forms.CharField(max_length = 250)
	