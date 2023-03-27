from ads.models import Ad, Comment
from rest_framework import serializers
from users.models import CustomUser
from users.serializers import CurrentUserSerializer


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    ad_id = serializers.IntegerField(source='ad.id', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_image = serializers.ImageField(source='author.image', read_only=True)

    class Meta:
        model = Comment
        fields = ('pk', 'text', 'author_id', 'ad_id', 'author_first_name', 'author_last_name', 'author_image')


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('pk', 'title', 'price', 'description')


class AdDetailSerializer(serializers.ModelSerializer):

    author_id = serializers.IntegerField(source='author.id')
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ('pk', 'title', 'price', 'author', 'author_id', 'author_first_name', 'author_last_name', 'phone', 'image')

    def get_author_first_name(self, obj):
        author_data = CurrentUserSerializer(obj.author).data
        return author_data.get('first_name')

    def get_author_last_name(self, obj):
        author_data = CurrentUserSerializer(obj.author).data
        return author_data.get('last_name')

    def get_phone(self, obj):
        author_data = CurrentUserSerializer(obj.author).data
        return author_data.get('phone')
