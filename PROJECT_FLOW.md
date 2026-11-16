# Website flow — TAZA FOOD CORNER

```mermaid
flowchart TD
    A[Home — TAZA FOOD CORNER] --> B[Delivery]
    A --> C[Dine-in]
    A --> D[Offers / Coupons / Sign in / Menu]
    B --> E[All Products — Page 2]
    C --> F[Outlet Finder — Page 3]
    F --> G[Allow location or choose manually]
    G --> H[Radius + Map + Outlet phone list]
    H --> I[Select outlet]
    I --> E
    E --> J[Add items / choose unit quantity]
    J --> K[Shopping Cart]
    K --> L[Checkout]
    L --> M[Confirmed Order — Page 4]
    M --> N[Payment Options — Page 5]
    N --> O[Order History / Staff / Delivery Management]
```

## Main systems

- Frontend: Django templates, HTML, CSS and JavaScript.
- Backend: Django views, forms, authentication and order/cart logic.
- REST API: Django REST Framework endpoints for nearby outlets, menu products and the signed-in customer's orders.
- Database: SQLite by default; MySQL supported for XAMPP.
- Map: Leaflet with OpenStreetMap tiles and browser geolocation.
- Admin: Django Admin for products, categories, outlets, coupons, orders and feedback.
