from rest_framework import generics
from product.models import Product
from product.models import ProductManager
from product.serializers import ProductSerializer
from rest_framework.response import Response
from . import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = None

        if request.user.is_authenticated:
            user = request.user.username
        
        query = request.GET.get('q')
        public = str(request.GET.get('public')) != "0"
        tag = request.GET.get('tag')
        
        if not query:
            return Response('', status=400)
            
        results = client.perform_search(query, tags=tag, user=user, public=public)

        return Response(results)    

class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        results = Product.objects.none()

        if query is not None:
            user = None

            if self.request.user.is_authenticated:
                user = self.request.user

            results = query_set.search(query, user=user)
        return results