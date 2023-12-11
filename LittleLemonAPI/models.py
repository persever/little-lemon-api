from django.db import models
from django.contrib.auth.models import User

currency_field = models.DecimalField(max_digits=6, decimal_places=2)

# class Cart(models.Model):
#     menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     price = currency_field
#     quantity = models.SmallIntegerField()
#     unit_price = currency_field
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('menuitem', 'user')

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
    price = currency_field
    title = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.featured:
            current_featured = MenuItem.objects.filter(featured=True).first()
            if (current_featured):
                current_featured.featured = False
                current_featured.save()
        super().save(*args, **kwargs)

class Order(models.Model):
    date = models.DateField(db_index=True)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = currency_field
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class OrderItem(models.Model):
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     price = currency_field
#     quantity = models.SmallIntegerField()
#     unit_price = currency_field

#     class Meta:
#         unique_together = ('menuitem', 'order')

class Rating(models.Model):
    menuitem_id = models.SmallIntegerField()
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)