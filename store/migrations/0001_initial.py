# Generated as the initial database schema for Taza Food Corner.
import decimal
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(max_length=90, unique=True)),
                ("description", models.CharField(blank=True, max_length=180)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "name"], "verbose_name_plural": "categories"},
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=30, unique=True)),
                ("description", models.CharField(blank=True, max_length=180)),
                ("discount_type", models.CharField(choices=[("PERCENT", "Percentage"), ("FIXED", "Fixed amount")], default="PERCENT", max_length=10)),
                ("discount_value", models.DecimalField(decimal_places=2, max_digits=8)),
                ("minimum_subtotal", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=9)),
                ("active", models.BooleanField(default=True)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("subject", models.CharField(blank=True, max_length=140)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_read", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Outlet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("address", models.CharField(max_length=220)),
                ("area", models.CharField(blank=True, max_length=100)),
                ("phone", models.CharField(max_length=30)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("opening_hours", models.CharField(default="10:00 AM – 10:00 PM", max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("is_demo", models.BooleanField(default=True, help_text="Keep enabled for seeded demo outlets. Replace with your real outlet details before launch.")),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(max_length=140, unique=True)),
                ("description", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=9)),
                ("image_url", models.URLField(blank=True, help_text="Optional image URL. Leave blank to use the built-in red/black/white product artwork.")),
                ("unit_label", models.CharField(default="piece", max_length=30)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="store.category")),
            ],
            options={"ordering": ["-is_featured", "name"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_number", models.CharField(editable=False, max_length=14, unique=True)),
                ("customer_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30)),
                ("fulfilment", models.CharField(choices=[("DELIVERY", "Delivery"), ("DINE_IN", "Dine-in")], default="DELIVERY", max_length=10)),
                ("delivery_address", models.TextField(blank=True)),
                ("special_instructions", models.TextField(blank=True)),
                ("coupon_code", models.CharField(blank=True, max_length=30)),
                ("subtotal", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=10)),
                ("delivery_fee", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=8)),
                ("discount", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=8)),
                ("total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=10)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("CONFIRMED", "Confirmed"), ("PREPARING", "Preparing"), ("READY", "Ready"), ("OUT_FOR_DELIVERY", "Out for delivery"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled")], default="PENDING", max_length=24)),
                ("payment_method", models.CharField(blank=True, choices=[("CASH", "Cash on delivery"), ("BKASH_DEMO", "bKash (demo only)"), ("CARD_DEMO", "Card (demo only)"), ("OUTLET", "Pay at outlet")], max_length=12)),
                ("payment_status", models.CharField(default="PENDING", max_length=12)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("coupon", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="store.coupon")),
                ("customer", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="taza_orders", to=settings.AUTH_USER_MODEL)),
                ("outlet", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to="store.outlet")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=120)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=9)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="store.order")),
                ("product", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="store.product")),
            ],
        ),
    ]
