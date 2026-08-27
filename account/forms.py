from django import forms
from django.contrib.auth.models import User

from products.models import product, category
from .models import Profile, Message, MessageReply


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=500)
    last_name = forms.CharField(max_length=500, required=False)
    email = forms.EmailField(max_length=100)
    phone_number = forms.CharField(max_length=50, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = Profile
        fields = [
            'phone_number', 'gender', 'address', 'city', 'country',
            'bio', 'profile_picture', 'payment_qr',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Your current password is incorrect.')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('New passwords do not match.')
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['name', 'category', 'price', 'stock', 'description', 'product_image', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = category.objects.all()
        self.fields['product_image'].required = False


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your message…'}),
        }


class MessageReplyForm(forms.ModelForm):
    class Meta:
        model = MessageReply
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your reply…'}),
        }
