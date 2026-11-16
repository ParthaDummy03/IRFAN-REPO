# Database design — TAZA FOOD CORNER

## Main entities

- **Category** 1-to-many **Product**: a category groups menu items.
- **Outlet** 1-to-many **Order**: an order can reference the selected outlet.
- **User** 1-to-many **Order**: an authenticated customer can view their own orders; guest checkout is also supported.
- **Order** 1-to-many **OrderItem**: the order stores an immutable item name/price snapshot and quantity.
- **Product** 1-to-many **OrderItem**: a nullable product reference preserves the order line if a menu item is deleted.
- **Coupon** 1-to-many **Order**: an order stores the coupon relationship and the applied coupon code.
- **Feedback** stores visitor feedback independently.

The cart is held in the Django session so guests can add items before signing in. Order lines are persisted in the database when checkout is submitted.

## ER diagram

```mermaid
erDiagram
    CATEGORY ||--o{ PRODUCT : contains
    PRODUCT ||--o{ ORDER_ITEM : selected_as
    ORDER ||--|{ ORDER_ITEM : contains
    OUTLET ||--o{ ORDER : fulfils_at
    USER ||--o{ ORDER : places
    COUPON ||--o{ ORDER : applied_to
    CATEGORY {
        bigint id PK
        varchar name
        varchar slug
        boolean is_active
    }
    PRODUCT {
        bigint id PK
        bigint category_id FK
        varchar name
        decimal price
        varchar unit_label
        boolean is_featured
        boolean is_available
    }
    OUTLET {
        bigint id PK
        varchar name
        varchar address
        varchar phone
        decimal latitude
        decimal longitude
    }
    ORDER {
        bigint id PK
        varchar order_number
        bigint customer_id FK
        bigint outlet_id FK
        varchar fulfilment
        decimal total
        varchar status
        varchar payment_status
    }
    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        varchar product_name
        decimal unit_price
        int quantity
    }
    COUPON {
        bigint id PK
        varchar code
        varchar discount_type
        decimal discount_value
    }
    USER {
        bigint id PK
        varchar username
        varchar email
    }
```

## Tables created by the included migration

`store_category`, `store_product`, `store_outlet`, `store_coupon`, `store_order`, `store_orderitem`, `store_feedback`, plus Django's built-in authentication/session/admin tables.
