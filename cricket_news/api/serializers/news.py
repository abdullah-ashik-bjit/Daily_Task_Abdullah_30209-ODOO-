from rest_framework import serializers
from news.models import News
from .user import UserSerializer

class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'pub_date', 'author', 'image']
        read_only_fields = ['pub_date', 'author']