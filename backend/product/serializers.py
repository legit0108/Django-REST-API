from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title_no_hello, unique_product_title
from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='pk', 
            read_only = True
    )

    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    title = serializers.CharField(validators = [validate_title_no_hello, unique_product_title])
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='product-edit' 
    )
    name = serializers.CharField(source='title', read_only=True)
    body = serializers.CharField(source='content')
    
    class Meta:
        model = Product
        fields = [
            'owner',
            'name',
            'edit_url',
            'url', 
            'pk',
            'title',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
        ]