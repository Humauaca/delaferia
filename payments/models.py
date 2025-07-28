from django.db import models
from django.contrib.auth.models import User
from item.models import Item

# Create your models here.

class Order(models.Model):

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="ordered_item")
    quantity_to_buy = models.IntegerField(default=1)
    price_per_unit_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.quantity_to_buy > self.item.quantity_in_stock:
            raise ValueError("Quantity to buy exceeds available stock.")
        
        self.item.quantity_in_stock -= self.quantity_to_buy
        self.item.save()

        # Save the price item at the buy time
        if not self.price_per_unit_at_purchase:
            self.price_per_unit_at_purchase = self.item.price
        self.total = self.price_per_unit_at_purchase * self.quantity_to_buy
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.status == 'paid'
    
    def mark_as_paid(self):
        self.status = 'paid'
        self.save()
        # Update the stock of the item
        self.item.quantity_in_stock -= self.quantity_to_buy
        self.item.save() # Save the item with the updated stock

    def __str__(self):
        return f'Orden de {self.buyer.username} para {self.item.name}'

class Payment(models.Model):
    PAYMENTS_STATUS = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Cancelado'),
        ('in_process', 'En proceso'),
    ]

    PAYMENT_PROVIDERS = [
        ('mercado_pago', 'Mercado Pago'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]



    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDERS, default='mercado_pago')
    payment_method = models.CharField(max_length=50)

    # Generic fields
    external_payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENTS_STATUS, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Specific data for each payment provider
    provider_data = models.JSONField(default=dict, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_method}" # type: ignore
    

class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_info')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    shipped_at = models.DateTimeField(null=True, blank=True)
