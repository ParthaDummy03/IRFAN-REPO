from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback, Outlet, Order

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=120, label="Full name")
    phone = forms.CharField(max_length=30, label="Phone number", widget=forms.TextInput(attrs={"placeholder": "01XXXXXXXXX"}))
    fulfilment = forms.ChoiceField(choices=Order.FULFILMENT_CHOICES, widget=forms.RadioSelect)
    outlet = forms.ModelChoiceField(queryset=Outlet.objects.filter(is_active=True), required=False, empty_label="Choose an outlet")
    delivery_address = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "House, road, area, city"}))
    coupon_code = forms.CharField(max_length=30, required=False, label="Coupon code")
    special_instructions = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Optional instructions"}))

    def __init__(self, *args, **kwargs):
        initial = kwargs.setdefault("initial", {})
        selected_outlet_id = kwargs.pop("selected_outlet_id", None)
        selected_mode = kwargs.pop("selected_mode", None)
        if selected_mode:
            initial.setdefault("fulfilment", selected_mode)
        if selected_outlet_id:
            initial.setdefault("outlet", selected_outlet_id)
        super().__init__(*args, **kwargs)
        self.fields["outlet"].queryset = Outlet.objects.filter(is_active=True)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
