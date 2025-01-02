'''
This module contains the views for the Articles app.
'''
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from articles.models import Article
from articles.serializers import ArticleSerializer

# Configure the logger
logger = logging.getLogger(__name__)

class ArticleDetail(APIView):
    """
    This class handles listing, creating, updating, and deleting Articles
    for a specific shipment.
    """

    def get(self, request, article_id, *args, **kwargs) -> Response:
        """
        Handle GET requests to retrieve an article by its ID.
        """
        logger.info("GET request received for article ID: %s", article_id)

        try:
            articles = Article.objects.filter(id=article_id)
            if not articles.exists():
                logger.warning("Article with ID %s not found", article_id)
                return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ArticleSerializer(articles, many=True)
            logger.info("Successfully retrieved article with ID: %s", article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error retrieving article with ID %s: %s", article_id, str(e))
            return Response({"error": "An error occurred"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ArticleSerializer)
    def put(self, request, article_id, *args, **kwargs) -> Response:
        """
        Handle PUT requests to update an existing Article completely.
        """
        logger.info("PUT request received for updating article ID: %s", article_id)

        try:
            article = Article.objects.get(id=article_id)
        except ObjectDoesNotExist as e:
            logger.warning("Article with ID %s not found for update", article_id)
            raise NotFound("Article not found for the given shipment") from e

        serializer = ArticleSerializer(article, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            logger.info("Successfully updated article with ID: %s", article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error("Failed to update article with ID %s: %s", article_id, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ArticleSerializer)
    def patch(self, request, article_id, *args, **kwargs) -> Response:
        """
        Handle PATCH requests to partially update an existing Article.
        """
        logger.info("PATCH request received for updating article ID: %s", article_id)

        try:
            article = Article.objects.get(id=article_id)
        except ObjectDoesNotExist as e:
            logger.warning("Article with ID %s not found for partial update", article_id)
            raise NotFound("Article not found for the given shipment") from e

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Successfully partially updated article with ID: %s", article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error("Failed to partially update article with ID %s: %s", 
                     article_id, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, *args, **kwargs) -> Response:
        """
        Handle DELETE requests to delete an existing Article.
        """
        logger.info("DELETE request received for deleting article ID: %s", article_id)

        try:
            article = Article.objects.get(id=article_id)
        except ObjectDoesNotExist as e:
            logger.warning("Article with ID %s not found for deletion", article_id)
            raise NotFound("Article not found for the given shipment") from e

        article.delete()
        logger.info("Successfully deleted article with ID: %s", article_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
