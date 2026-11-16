from math import asin, cos, radians, sin, sqrt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Outlet, Product, Order


def distance_km(lat1, lon1, lat2, lon2):
    radius = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * radius * asin(sqrt(a))


@api_view(["GET"])
@permission_classes([AllowAny])
def nearby_outlets(request):
    try:
        lat = float(request.query_params["lat"])
        lng = float(request.query_params["lng"])
        radius = float(request.query_params.get("radius", "10"))
        if not (-90 <= lat <= 90 and -180 <= lng <= 180 and 1 <= radius <= 100):
            raise ValueError
    except (KeyError, TypeError, ValueError):
        lat = lng = radius = None

    rows = []
    for outlet in Outlet.objects.filter(is_active=True):
        item = {
            "id": outlet.id,
            "name": outlet.name,
            "address": outlet.address,
            "area": outlet.area,
            "phone": outlet.phone,
            "latitude": float(outlet.latitude),
            "longitude": float(outlet.longitude),
            "opening_hours": outlet.opening_hours,
            "is_demo": outlet.is_demo,
            "distance_km": None,
        }
        if lat is not None:
            item["distance_km"] = round(distance_km(lat, lng, item["latitude"], item["longitude"]), 2)
            if item["distance_km"] > radius:
                continue
        rows.append(item)
    if lat is not None:
        rows.sort(key=lambda row: row["distance_km"])
    return Response({"count": len(rows), "radius_km": radius, "results": rows})


@api_view(["GET"])
@permission_classes([AllowAny])
def products_api(request):
    products = Product.objects.filter(is_available=True).select_related("category")
    category = request.query_params.get("category")
    if category:
        products = products.filter(category__slug=category)
    return Response({"count": products.count(), "results": [
        {"id": p.id, "name": p.name, "slug": p.slug, "category": p.category.name,
         "description": p.description, "price": str(p.price), "unit": p.unit_label,
         "image_url": p.image_url, "featured": p.is_featured}
        for p in products
    ]})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders_api(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related("items")
    return Response({"count": orders.count(), "results": [{
        "order_number": order.order_number,
        "created_at": order.created_at.isoformat(),
        "fulfilment": order.fulfilment,
        "status": order.status,
        "payment_status": order.payment_status,
        "total": str(order.total),
        "items": [{"name": item.product_name, "quantity": item.quantity, "line_total": str(item.line_total)} for item in order.items.all()],
    } for order in orders]})
