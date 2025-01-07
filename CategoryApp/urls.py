from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    UserCategoryPreferenceListCreateView,
    UserCategoryPreferenceDeleteView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(),
         name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),
    path('preferences/', UserCategoryPreferenceListCreateView.as_view(),
         name='user-preference-list-create'),
    path('preferences/<int:category_id>/',
         UserCategoryPreferenceDeleteView.as_view(), name='user-preference-delete'),
]
