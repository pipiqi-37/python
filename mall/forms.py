from django import forms

from mall.models import Product


class ProAdmin(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["updated_at", "created_at"]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if int(price) <= 0:
            raise forms.ValidationError("销售价格不能小于0")
        return price