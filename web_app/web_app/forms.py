from django import forms


class TableForm(forms.Form):
    num = forms.IntegerField(label='Please Enter Number:')
