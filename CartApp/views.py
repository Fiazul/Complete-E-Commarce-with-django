from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from ProductApp.models import Product
from .serializers import CartSerializer, CartItemSerializer


class CartView(APIView):
    """Handle retrieving and managing the user's cart."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the authenticated user's cart."""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        """Add a product to the user's cart."""
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemView(APIView):
    """Handle updating or deleting specific cart items."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        """Update the quantity of a cart item."""
        try:
            cart_item = CartItem.objects.get(
                id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if quantity is not None:
            if int(quantity) <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

        cart = cart_item.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        """Remove a product from the cart."""
        try:
            cart_item = CartItem.objects.get(
                id=item_id, cart__user=request.user)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart = cart_item.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
