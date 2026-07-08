from django import forms
from myapp.models import Products

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name','price','description','image','stock']


    def cleen_price(self):
        product_price = self.cleaned_data['price']
        if product_price < 0:
            raise forms.ValidationError("price can not be negative")
        return product_price