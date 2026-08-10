from myapp.models import Products
from decimal import Decimal

class Cart():
    def __init__(self,request):
        self.session = request.session
        cart = request.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart']={}
        self.cart = cart

    def __len__(self):
        return sum(int(item['qty']) for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * Decimal(item['qty']) for item in self.cart.values())
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)

        # shallow copy of the outer dict; inner dicts must be copied to avoid
        # mutating session-stored objects. Otherwise converting price to
        # Decimal here will make session contain Decimal objects which are
        # not JSON serializable and will break session.save().
        cart = {k: v.copy() for k, v in self.cart.items()}

        for product in products:
            if str(product.id) in cart:
                cart[str(product.id)]['product'] = product

        for item in cart.values():
            # ensure numeric fields are proper types for display/calculation
            item['price'] = Decimal(item['price'])
            try:
                item['qty'] = int(item['qty'])
            except Exception:
                item['qty'] = int(Decimal(str(item.get('qty', 0))))
            item['total'] = item['price'] * Decimal(item['qty'])
            yield item

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * Decimal(item['qty'])
            for item in self.cart.values()
        )

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
        self.session.modified = True

    def delete(self,product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True

    def update(self, product, product_qty):
        product_id = str(product)
        product_quantity = product_qty
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
        self.session.modified = True
    

    