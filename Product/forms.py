from django import forms
from .models import Order

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        labels = {
            'product_id': '商品id',
            'qty': '購買數量',
            'customer_id': '顧客id'
        }
    def clean_email(self, *args, **kwargs):
        product_id = self.cleaned_data.get('product_id') #取得樣板所填寫的資料
        if product_id == 'Select Product':
            messages.error(request, '請選擇商品!')
        return product_id