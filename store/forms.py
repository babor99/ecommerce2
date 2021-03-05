from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
		widgets = {
		'email': forms.EmailInput(attrs={'class':'form-control', 'type':'email'}),
		'subject': forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
		'message': forms.Textarea(attrs={'class':'form-control', 'rows':'4'}),
		}
