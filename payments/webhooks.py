# import stripe
# from django.conf import settings
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# from orders.models import Order
# from cart.models import CartItem


# stripe.api_key = settings.STRIPE_SECRET_KEY


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
# # 
#     try:
#         event = stripe.Webhook.construct_event(
#             payload=payload,
#             sig_header=sig_header,
#             secret=settings.STRIPE_WEBHOOK_SECRET,
#         )
#     except ValueError:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # ==================================================
#     # ✅ CHECKOUT PAYMENT SUCCESS (MOST IMPORTANT EVENT)
#     # ==================================================
#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]

#         order_id = session["metadata"].get("order_id")
#         payment_intent = session.get("payment_intent")

#         try:
#             order = Order.objects.get(id=order_id)

#             # 🔐 Prevent duplicate webhook execution
#             if not order.is_paid:
#                 order.is_paid = True
#                 order.status = "pending"
#                 order.transaction_id = payment_intent
#                 order.save()

#                 # 🔥 CLEAR CART AFTER SUCCESSFUL PAYMENT
#                 CartItem.objects.filter(cart__user=order.user).delete()

#         except Order.DoesNotExist:
#             pass

#     return HttpResponse(status=200)
