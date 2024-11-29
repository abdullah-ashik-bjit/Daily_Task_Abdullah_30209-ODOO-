from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from news.models import News
from ..serializers.news import NewsSerializer
from ..permissions import IsAuthorOrReadOnly

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-pub_date')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['pub_date', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_articles(self, request):
        articles = News.objects.filter(author=request.user)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)