from django.contrib import admin
from .models import Category, Product, Outlet, Coupon, Order, OrderItem, Feedback

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("sort_order", "is_active")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "unit_label", "is_featured", "is_available")
    list_filter = ("category", "is_featured", "is_available")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_editable = ("price", "is_featured", "is_available")

@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "phone", "is_active", "is_demo")
    list_filter = ("is_active", "is_demo")
    search_fields = ("name", "address", "area", "phone")

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "discount_value", "active", "ends_at")
    list_filter = ("active", "discount_type")
    search_fields = ("code",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer_name", "phone", "fulfilment", "total", "status", "payment_status", "created_at")
    list_filter = ("status", "fulfilment", "payment_status", "created_at")
    search_fields = ("order_number", "customer_name", "phone")
    readonly_fields = ("order_number", "subtotal", "delivery_fee", "discount", "total", "created_at", "updated_at")
    inlines = [OrderItemInline]

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("is_read",)

admin.site.site_header = "TAZA FOOD CORNER — ADMINISTRATION"
admin.site.site_title = "Taza Admin"
admin.site.index_title = "Manage menu, outlets, coupons and orders"
