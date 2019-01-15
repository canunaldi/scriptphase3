from django import forms

class NameForm(forms.Form):
    question = forms.IntegerField(label = 'question')
    deneme = forms.CharField(label = 'deneme')