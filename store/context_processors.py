def cart_summary(request):
    cart = request.session.get("taza_cart", {})
    count = 0
    for quantity in cart.values():
        try:
            count += max(0, int(quantity))
        except (TypeError, ValueError):
            continue
    return {"cart_count": count}
