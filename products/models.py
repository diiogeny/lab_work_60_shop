from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    category = models.CharField(max_length=100, verbose_name="Категория")
    quantity = models.PositiveIntegerField(verbose_name="Остаток на складе")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя пользователя")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    def __str__(self):
        return f"Заказ {self.id} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} x {self.quantity} для {self.order.name}"