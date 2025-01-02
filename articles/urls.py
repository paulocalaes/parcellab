from django.urls import path
from .views.article_detail import ArticleDetail

urlpatterns = [
    path('<int:article_id>/', ArticleDetail.as_view(), name='article-detail'),
]