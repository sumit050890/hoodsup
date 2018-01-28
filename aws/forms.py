from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.CharField(label="Email Address", required=True, max_length=32)
    email2 = forms.CharField(label="Confirm Email", required=True, max_length=32)
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email2', 'email', 'password']

    # def clean(self,*args, **kwargs):
    #     email = self.cleaned_data("email")
    #     email2 = self.cleaned_data("email2")
    #     if email != email2:
    #         raise forms.ValidationError("Emails must match")
    #
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exist():
    #         raise forms.ValidationError("This email has already been registered")
    #     return super(UserRegistrationForm,self).clean(*args, **kwargs)

    def clean_email(self, *args, **kwargs):

        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email != email2:
            raise forms.ValidationError("Emails must match")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        user = authenticate(username=username, password=password)
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 1:
            user = user_qs.first()
        if username and password:
            if not user:
                raise forms.ValidationError("This user does not exist!! Please Try Again")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("This user no longer exist")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class AWSInstanceForm(forms.ModelForm):
    aws_instance_type = forms.CharField(
        required=True,
        label='Instance Type',
        max_length=32
    )
    aws_availability_zone = forms.CharField(
        required=True,
        label='Availability Zone',
        max_length=32
    )
    aws_storage_type = forms.CharField(
        required=True,
        label='Storage',
        max_length=32
    )

    class Meta:
        model = User
        fields = [ 'aws_instance_type', 'aws_availability_zone', 'aws_storage_type']




    def clean(self, *args, **kwargs):
        aws_instance_type = self.cleaned_data.get("aws_instance_type")
        aws_availability_zone = self.cleaned_data.get("aws_availability_zone")
        aws_storage_type = self.cleaned_data.get("aws_storage_type")
        if not (aws_storage_type and aws_availability_zone and aws_instance_type):
                raise forms.ValidationError("This user not authenticated")

        return super(AWSInstanceForm, self).clean(*args, **kwargs)


