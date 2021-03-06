from .utils import *


class NewSubcontractForm(ModelForm):
    expire_date = forms.CharField(required=False,
                                  label="تاریخ اعتبار",
                                  widget=forms.TextInput(attrs={'placeholder': '1400/01/01'}))

    value_in_rial = forms.CharField(required=False, label="مبلغ به ریال")
    remittance_value = forms.CharField(required=False, label="مبلغ حواله")

    def __init__(self, parent: NormalContract = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['id'].initial = 0
        self.fields['dst_owner_bank_account_id'].required = False
        self.fields['description'].required = False

    def save(self, commit=True):
        m = super(NewSubcontractForm, self).save(commit=False)
        m.status = ContractStatus.NONE
        if commit:
            m.save()
        return m

    def clean_dst_owner_bank_account_id(self):

        dst_owner_bank_account_id = self.cleaned_data['dst_owner_bank_account_id']
        empty_field_validator(dst_owner_bank_account_id)

        # dst_owner = Owner.objects.get(pk=dst_owner_bank_account_id)
        dst_owner = get_public_owner(dst_owner_bank_account_id)

        if dst_owner and dst_owner.owner_type == OwnerType.EXPORTER:
            return dst_owner
        else:
            raise forms.ValidationError("خطا: صادرکننده با این مشخصات در سامانه ثبت نشده است!")

        # except Owner.DoesNotExist:
        #     raise forms.ValidationError("خطا: صراف با این مشخصات در سامانه ثبت نشده است!")

    def clean_value_in_rial(self):
        value_in_rial = self.cleaned_data['value_in_rial']
        empty_field_validator(value_in_rial)
        int_value_in_rial = int(value_in_rial.replace(',', ''))
        if int_value_in_rial <= 0:
            raise forms.ValidationError("خطا: مبلغ قرار داد باید بیشتر از صفر باشد!")
        if int_value_in_rial > self.parent.available_value_in_rial:
            raise forms.ValidationError("خطا: مبلغ وارد شده بیشتر از موجودی قرار داد صراف و واردکننده است!")
        return int_value_in_rial

    def clean_remittance_value(self):
        remittance_value = self.cleaned_data['remittance_value']
        empty_field_validator(remittance_value)
        int_remittance_value = int(remittance_value.replace(',', ''))
        if int_remittance_value <= 0:
            raise forms.ValidationError("خطا: مبلغ حواله باید بیشتر از صفر باشد!")
        return int_remittance_value

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        empty_field_validator(expire_date)
        try:
            tmp = jdate2timestamp(expire_date)
            if tmp > self.parent.expire_date:
                raise forms.ValidationError(
                    "خطا: تاریخ وارد شده باید قبل از تاریخ وارد شده برای فرارداد صراف و واردکننده باشد!")
            else:
                return tmp
        except ValueError as err:
            raise forms.ValidationError("خطا: تاریخ وارد شده صحیح نمی باشد!")

    def clean(self):
        if not self.parent.is_parentable:
            raise forms.ValidationError(
                "خطا:قرار داد بین وارد کننده و صراف از نوع تک تسویه ای است و امکان عقد قرار داد دیگری وجود ندارد!")
        super().clean()

    class Meta:
        model = Subcontract
        fields = [
            'id',
            'dst_owner_bank_account_id',
            'value_in_rial',
            'remittance_value',
            'expire_date',
            'description',
        ]

        labels = {
            'expire_date': 'تاریخ اعتبار',
            'remittance_value': 'مبلغ حواله',
            'description': 'توضیحات',
            'src_owner_bank_account_id': 'شماره حساب صراف',
            'dst_owner_bank_account_id': 'شماره حساب صادرکننده',
        }
        help_texts = {
            'expire_date': 'با فرمت YYYY/MM/DD',
        }
