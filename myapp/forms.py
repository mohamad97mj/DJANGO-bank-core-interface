from django import forms
from django.forms import ModelForm, TextInput, Form
from .models import AuthProfile, UserProfile, JudgeProfile, Transaction, Contract, Subcontract
from django.utils.translation import gettext_lazy as _

LOGIN_ROLES = [
    ('user', 'کاربر حساب'),
    ('judge', 'داور'),
]


class LoginForm(Form):
    role = forms.CharField(label='ورود به سامانه به عنوان', widget=forms.Select(choices=LOGIN_ROLES),
                           help_text="")
    username = forms.CharField(max_length=255, label="نام کاربری*", required=False,
                               help_text="به صورت پیش فرض همان کد ملی شماست")
    password = forms.CharField(max_length=32, label="گذرواژه*", widget=forms.PasswordInput, required=False,
                               help_text="")

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if username != "mohamad":
    #         raise forms.ValidationError("خطا: این کاربر وجود ندارد!")
    #     else:
    #         return username


class UserProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['national_code'].widget.attrs['disabled'] = True
        self.fields['first_name'].widget.attrs['disabled'] = True
        self.fields['last_name'].widget.attrs['disabled'] = True

    class Meta:
        model = UserProfile
        fields = ['national_code', 'first_name', 'last_name']
        labels = {
            'national_code': 'کد ملی',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }


class JudgeProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['national_id'].widget.attrs['disabled'] = True
        self.fields['name'].widget.attrs['disabled'] = True

    class Meta:
        model = JudgeProfile
        fields = ['national_id', 'name']
        labels = {
            'national_id': 'شناسه ملی',
            'name': 'نام',
        }


class ContractDetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['src_owner'].widget.attrs['disabled'] = True
        self.fields['dst_owner'].widget.attrs['disabled'] = True
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['settlement_type'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_currency'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True

    class Meta:
        model = Contract
        fields = ['id', 'src_owner', 'dst_owner', 'expire_date', 'settlement_type', 'value_in_rial',
                  'remittance_currency', 'remittance_value',
                  'judge', 'status', 'description', 'judge_vote']
        labels = {
            'id': 'شناسه',
            'src_owner': 'شماره حساب مبداء',
            'dst_owner': 'شماره حساب مقصد',
            'expire_date': 'تاریخ اعتبار',
            'settlement_type': 'نوع تسویه',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'judge': 'شناسه ملی داور',
            'status': 'وضعیت',
            'judge_vote': 'رای داور',
            'description': 'توضیحات',
        }


class NewContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['dst_owner', 'expire_date', 'settlement_type', 'value_in_rial', 'remittance_currency',
                  'remittance_value',
                  'judge', 'description']
        labels = {
            'dst_owner': 'شماره حساب مقصد',
            'expire_date': 'تاریخ اعتبار',
            'settlement_type': 'نوع تسویه',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'judge': 'شناسه ملی داور',
            'description': 'توضیحات',
        }


class SubcontractDetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['dst_owner'].widget.attrs['disabled'] = True
        self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True

    class Meta:
        model = Subcontract
        fields = ['id', 'expire_date', 'value_in_rial', 'remittance_value',
                  'status', 'description', 'judge_vote', 'dst_owner']
        labels = {
            'id': 'شناسه',
            'expire_date': 'تاریخ اعتبار',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'status': 'وضعیت',
            'judge_vote': 'رای داور',
            'description': 'توضیحات',
            'dst_owner': 'شماره حساب طرف دیگر قرارداد',
        }


class NewSubcontractForm(ModelForm):
    class Meta:
        model = Subcontract
        fields = ['expire_date', 'value_in_rial', 'remittance_value', 'status', 'description', 'dst_owner']
        labels = {
            'expire_date': 'تاریخ اعتبار',
            'value_in_rial': 'مبلغ به ریال',
            'remittance_value': 'مبلغ حواله',
            'status': 'وضعیت',
            'description': 'توضیحات',
            'dst_owner': 'شماره حساب طرف دیگر قرار داد',
        }


class TransactionDetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['disabled'] = True
        self.fields['transaction_type'].widget.attrs['disabled'] = True
        self.fields['otherside_owner'].widget.attrs['disabled'] = True
        self.fields['value'].widget.attrs['disabled'] = True
        self.fields['operator_type'].widget.attrs['disabled'] = True
        self.fields['operator'].widget.attrs['disabled'] = True

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'otherside_owner', 'value', 'operator_type', 'operator']
        labels = {
            'id': 'شناسه',
            'transaction_type': 'نوع تراکنش',
            'otherside_owner': 'شماره حساب طرف دیگر تراکنش',
            'value': 'مبلغ',
            'operator_type': 'نوع اپراتور',
            'operator': 'کد ملی اپراتور',
        }


class NewTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['otherside_owner', 'value']
        labels = {
            'otherside_owner': 'شماره حساب مقصد',
            'value': 'مبلغ',
        }
