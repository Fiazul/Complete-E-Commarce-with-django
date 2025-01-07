from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, UserCategoryPreference
from .serializers import CategorySerializer, UserCategoryPreferenceSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(
        parent=None)  # Fetch top-level categories
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserCategoryPreferenceListCreateView(generics.ListCreateAPIView):
    serializer_class = UserCategoryPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserCategoryPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCategoryPreferenceDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, category_id):
        try:
            preference = UserCategoryPreference.objects.get(
                user=request.user, category_id=category_id)
            preference.delete()
            return Response({'message': 'Preference removed successfully.'}, status=204)
        except UserCategoryPreference.DoesNotExist:
            return Response({'error': 'Preference not found.'}, status=404)
