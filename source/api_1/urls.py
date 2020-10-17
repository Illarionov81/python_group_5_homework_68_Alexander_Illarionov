from django.urls import path

from api_1.views import get_token_view, ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView

app_name = 'api_v1'

urlpatterns = [
    path('get_token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_view'),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name='article_update')
]
