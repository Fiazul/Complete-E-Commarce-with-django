from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ProductApp.models import Product
from CategoryApp.models import Category
from .serializers import SearchHistorySerializer
from .models import SearchHistory
from ProductApp.serializers import ProductSerializer
from CategoryApp.serializers import CategorySerializer
from .aisearch import generate_keyword

from django.db.models import Q


class StandardSearchView(APIView):
    """
    Handles product and category searches based on a keyword.
    Stores the search query in the database.
    """

    def get(self, request):
        keyword = request.query_params.get('q', '').strip()

        if not keyword:
            return Response(
                {"detail": "Please provide a search keyword using the 'q' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        SearchHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            query=keyword
        )

        product_results = Product.objects.filter(
            name__icontains=keyword, is_active=True)

        category_results = Category.objects.filter(
            name__icontains=keyword, is_active=True)

        category_products = Product.objects.filter(
            category__name__icontains=keyword, is_active=True
        )

        # Structure the response
        response_data = {
            "products": ProductSerializer(product_results, many=True).data,
            "categories": CategorySerializer(category_results, many=True).data,
            "category_products": ProductSerializer(category_products, many=True).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AISearchView(APIView):
    """
    AI-powered product search based on keywords or prompts.
    """

    def get(self, request):
        # Extract the search query
        keyword = request.query_params.get('q', '').strip()

        if not keyword:
            return Response(
                {"detail": "Please provide a search keyword using the 'q' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save search history
        SearchHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            query=keyword
        )

        # Generate relevant keywords using the Generative AI API
        product_category_list = ", ".join(
            Category.objects.values_list('name', flat=True)
        )
        ai_keywords = generate_keyword(keyword, product_category_list)
        keywords_list = [kw.strip()
                         for kw in ai_keywords.split("\n") if kw.strip()]

        response_data = {}

        for ai_keyword in keywords_list:

            matching_categories = Category.objects.filter(
                Q(name__icontains=ai_keyword) | Q(
                    description__icontains=ai_keyword)
            )

            subcategories = Category.objects.filter(
                parent__in=matching_categories)

            all_categories = matching_categories | subcategories

            product_results = Product.objects.filter(
                Q(category__in=all_categories) |
                Q(name__icontains=ai_keyword)
            )

            # Add results to the response
            response_data[ai_keyword] = {
                "ai_keywords": ai_keyword,
                "products": ProductSerializer(product_results, many=True).data,
            }

        return Response(response_data, status=status.HTTP_200_OK)


class UserSearchHistoryView(APIView):
    """
    Retrieves the search history for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch search history for the logged-in user
        search_histories = SearchHistory.objects.filter(
            user=request.user).order_by('-timestamp')
        serializer = SearchHistorySerializer(search_histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllSearchHistoryView(APIView):
    """
    Admin-only endpoint to retrieve all search history.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        search_histories = SearchHistory.objects.all().order_by('-timestamp')
        serializer = SearchHistorySerializer(search_histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
