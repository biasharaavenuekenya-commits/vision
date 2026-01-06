# main/forms.py
from django import forms
from .models import Subscriber

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (Optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us why you\'re interested in VISION 2026',
                'rows': '3'
            }),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email