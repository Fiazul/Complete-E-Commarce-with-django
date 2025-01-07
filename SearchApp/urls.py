from django.urls import path
from .views import UserSearchHistoryView, AllSearchHistoryView, StandardSearchView, AISearchView

urlpatterns = [
    path('history/', UserSearchHistoryView.as_view(), name='user-search-history'),
    path('admin/history/', AllSearchHistoryView.as_view(),
         name='all-search-history'),
    path('search/', StandardSearchView.as_view(), name='standard-search'),
    path('ai-search/', AISearchView.as_view(), name='ai-search'),
]
