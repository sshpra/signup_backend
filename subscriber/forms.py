from django import forms


class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'required': True
        }),
        label='Email Address'
    )
    
    name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name (optional)'
        }),
        label='Name (Optional)'
    )

