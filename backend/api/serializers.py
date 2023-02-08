from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='pk', 
            read_only = True
    )

    title = serializers.CharField(read_only=True)

    email = serializers.EmailField(write_only = False)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)