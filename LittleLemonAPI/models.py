from datetime import date
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def str(self)-> str:
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    featured = models.BooleanField(db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.featured:
            current_featured = MenuItem.objects.filter(featured=True).first()
            if (current_featured):
                current_featured.featured = False
                current_featured.save()
        return super().save(*args, **kwargs)

class Order(models.Model):
    date = models.DateField(db_index=True)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.date = date.today()
        return super().save(*args, **kwargs)

class PurchaseItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)

    class Meta:
        abstract = True

class CartItem(PurchaseItem):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['menu_item', 'user'], name='Item already in cart.'),
        ]

class OrderItem(PurchaseItem):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['menu_item', 'order'], name='Item already in order.'),
        ]

class Rating(models.Model):
    menuitem_id = models.SmallIntegerField()
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)