from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .api_views import distance_km
from .models import Category, Product, Outlet, Order


class TazaWebsiteTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Burgers", slug="burgers", sort_order=1)
        self.product = Product.objects.create(
            category=self.category,
            name="Taza Test Burger",
            slug="taza-test-burger",
            description="Test menu item",
            price=Decimal("250.00"),
            unit_label="piece",
            is_available=True,
            is_featured=True,
        )
        self.outlet = Outlet.objects.create(
            name="Taza Test Outlet",
            address="Test address",
            area="Test area",
            phone="01000000000",
            latitude=Decimal("22.356900"),
            longitude=Decimal("91.783200"),
            opening_hours="10:00 AM – 10:00 PM",
            is_active=True,
            is_demo=True,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TAZA FOOD CORNER")

    def test_products_api_returns_active_item(self):
        response = self.client.get(reverse("api_products"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["name"], "Taza Test Burger")

    def test_nearby_api_returns_distance(self):
        response = self.client.get(reverse("api_nearby_outlets"), {
            "lat": "22.3569", "lng": "91.7832", "radius": "10"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["distance_km"], 0.0)

    def test_distance_calculation(self):
        self.assertAlmostEqual(distance_km(22.0, 91.0, 22.0, 91.0), 0.0, places=5)

    def test_guest_can_add_item_to_cart(self):
        response = self.client.post(reverse("add_to_cart", args=[self.product.id]), {
            "quantity": "2", "next": "/menu/"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["taza_cart"][str(self.product.id)], 2)
        cart_response = self.client.get(reverse("cart"))
        self.assertEqual(cart_response.status_code, 200)
        self.assertContains(cart_response, "Taza Test Burger")

    def test_guest_can_place_delivery_order(self):
        self.client.post(reverse("add_to_cart", args=[self.product.id]), {
            "quantity": "1", "next": "/menu/"
        })
        response = self.client.post(reverse("checkout"), {
            "customer_name": "Test Customer",
            "phone": "01700000000",
            "fulfilment": Order.DELIVERY,
            "delivery_address": "Test Road, Chattogram",
            "coupon_code": "",
            "special_instructions": "",
        })
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(customer_name="Test Customer")
        self.assertEqual(order.total, Decimal("310.00"))
        self.assertEqual(order.items.count(), 1)
