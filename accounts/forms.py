from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms

class BootstrapMixin:
	field_names = None
	def __init__(self, *args, **kwargs):
		super(BootstrapMixin, self).__init__(*args, **kwargs)
		if self.field_names:
			for fieldname in self.field_names:
				self.fields[fieldname].widget.attrs={'class':'form-control'}
		else:
			raise ValueError('The field name must be set.')
		 


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class PasswordChangingForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
	class Meta:
		model = User
		fields = ['old_password', 'new_password1', 'new_password2']
 

class MyPasswordResetForm(BootstrapMixin, PasswordResetForm):
	field_names = ['email',]
	def clean_email(self):
		email = self.cleaned_data['email']
		if not User.objects.filter(email__iexact=email, is_active=True).exists():
			msg = "There is no user registered with the specified email address."
			self.add_error('email', msg)
		return email


class MySetPasswordResetForm(BootstrapMixin, SetPasswordForm):
	field_names = ['new_password1', 'new_password2',]

