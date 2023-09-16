# forms.py 파일에 추가
from django import forms


class SearchForm(forms.Form):
    sentence = forms.CharField(label='문장을 입력하세요', widget=forms.TextInput(attrs={'class': 'form-control'}))

