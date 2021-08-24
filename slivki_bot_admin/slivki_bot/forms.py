from django import forms
from slivki_bot.models import Employee
from slivki_bot.models import Users, Messages


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = "__all__"


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = "__all__"