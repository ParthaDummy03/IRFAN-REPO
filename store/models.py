import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    description = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.URLField(blank=True, help_text="Optional image URL. Leave blank to use the built-in red/black/white product artwork.")
    unit_label = models.CharField(max_length=30, default="piece")
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return self.name


class Outlet(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    area = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    opening_hours = models.CharField(max_length=100, default="10:00 AM – 10:00 PM")
    is_active = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=True, help_text="Keep enabled for seeded demo outlets. Replace with your real outlet details before launch.")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Coupon(models.Model):
    PERCENT = "PERCENT"
    FIXED = "FIXED"
    DISCOUNT_TYPES = [(PERCENT, "Percentage"), (FIXED, "Fixed amount")]

    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=180, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default=PERCENT)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    minimum_subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("0.00"))
    active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self, subtotal):
        now = timezone.now()
        return (
            self.active
            and subtotal >= self.minimum_subtotal
            and (self.starts_at is None or self.starts_at <= now)
            and (self.ends_at is None or self.ends_at >= now)
        )

    def calculate_discount(self, subtotal):
        if self.discount_type == self.PERCENT:
            amount = subtotal * self.discount_value / Decimal("100")
        else:
            amount = self.discount_value
        return min(subtotal, amount).quantize(Decimal("0.01"))

    def __str__(self):
        return self.code


class Order(models.Model):
    DELIVERY = "DELIVERY"
    DINE_IN = "DINE_IN"
    FULFILMENT_CHOICES = [(DELIVERY, "Delivery"), (DINE_IN, "Dine-in")]

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (PENDING, "Pending"), (CONFIRMED, "Confirmed"), (PREPARING, "Preparing"),
        (READY, "Ready"), (OUT_FOR_DELIVERY, "Out for delivery"),
        (COMPLETED, "Completed"), (CANCELLED, "Cancelled"),
    ]

    CASH = "CASH"
    BKASH_DEMO = "BKASH_DEMO"
    CARD_DEMO = "CARD_DEMO"
    OUTLET = "OUTLET"
    PAYMENT_CHOICES = [
        (CASH, "Cash on delivery"),
        (BKASH_DEMO, "bKash (demo only)"),
        (CARD_DEMO, "Card (demo only)"),
        (OUTLET, "Pay at outlet"),
    ]

    order_number = models.CharField(max_length=14, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="taza_orders")
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    fulfilment = models.CharField(max_length=10, choices=FULFILMENT_CHOICES, default=DELIVERY)
    outlet = models.ForeignKey(Outlet, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    delivery_address = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    coupon_code = models.CharField(max_length=30, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(max_length=12, choices=PAYMENT_CHOICES, blank=True)
    payment_status = models.CharField(max_length=12, default="PENDING")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} — {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=120)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=140, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback from {self.name}"
