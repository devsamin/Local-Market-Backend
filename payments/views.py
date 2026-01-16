


# payments/views.py
import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_stripe_checkout(request):
    order_id = request.data.get("order_id")

    if not order_id:
        return Response({"error": "Order ID is required"}, status=400)

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    line_items = []

    for item in order.items.all():
        product = item.product

        if not product.discounted_price:
            return Response({"error": f"{product.name} has no price"}, status=400)

        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product.name,
                },
                "unit_amount": int(float(product.discounted_price) * 100),
            },
            "quantity": item.quantity,
        })

    success_url = f"https://local-market-coral.vercel.app/payment-success?order_id={order.id}"
    cancel_url = "https://local-market-coral.vercel.app/cart"

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"order_id": order.id},
        )
    except Exception as e:
        print("Stripe Error:", str(e))
        return Response({"error": str(e)}, status=500)

    return Response({"checkout_url": session.url})

from cart.models import CartItem

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_success(request):
    order_id = request.GET.get("order_id")

    if not order_id:
        return Response({"error": "Order ID missing"}, status=400)

    try:
        order = Order.objects.get(id=order_id, user=request.user)

        if not order.is_paid:
            order.is_paid = True
            order.status = "pending"
            order.save()

            # 🔥 CART CLEAR
            CartItem.objects.filter(cart__user=request.user).delete()

        return Response({"message": "Payment confirmed & cart cleared"})

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

