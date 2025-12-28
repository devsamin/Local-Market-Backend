from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from orders.models import OrderItem
from products.models import Product
from reviews.models import Review

class SellerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = request.user  # current logged-in seller

        # Get all orders for this seller
        orders = OrderItem.objects.filter(seller=seller)
        products = Product.objects.filter(seller=seller)
        reviews = Review.objects.filter(product__seller=seller)

        # Summary stats
        total_earnings = sum(o.price * o.quantity for o in orders)
        products_sold = sum(o.quantity for o in orders)
        orders_count = {
            'pending': orders.filter(order__status='pending').count(),
            'completed': orders.filter(order__status='delivered').count(),
            'cancelled': orders.filter(order__status='cancelled').count(),
        }
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        # Recent 5 orders
        recent_orders = [
            {
                'id': o.order.id,
                'product_name': o.product.name,
                'quantity': o.quantity,
                'price': o.price,
                'status': o.order.status
            } 
            for o in orders.order_by('-order__created_at')[:5]
        ]

        # Recent 5 reviews
        recent_reviews = [
            {
                'customer': r.user.get_full_name() if r.user else "Guest",
                'product': r.product.name,
                'rating': r.rating,
                'comment': r.comment,
                'date': r.created_at.strftime("%d %b %Y")
            }
            for r in reviews.order_by('-created_at')[:5]
        ]

        data = {
            'total_earnings': total_earnings,
            'products_sold': products_sold,
            'orders_count': orders_count,
            'average_rating': round(avg_rating, 1),
            'recent_orders': recent_orders,
            'recent_reviews': recent_reviews,
        }

        return Response(data)
