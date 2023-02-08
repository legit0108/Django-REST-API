from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixin
)

class ProductCreateAPIView(StaffEditorPermissionMixin, generics.CreateAPIView):
    querySet = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if content is None:
            content = title
        serializer.save(content=content)

product_create_view = ProductCreateAPIView.as_view()


class ProductListCreateAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if not content:
            content = title
        serializer.save(user=self.request.user, content=content)
     
product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(UserQuerySetMixin, StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
    ):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        primary_key = kwargs.get("pk")
        if primary_key is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if content is None:
            content = "this is a single view doing cool stuff!"
        serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()


# below function is the functional-based view equivalent for create, retrieve, list

@api_view(["GET", "POST"])
def product_alt_view(request, primary_key=None, *args, **kwargs):
    method = request.method

    if method == "GET":
       if primary_key is not None:
           obj = get_object_or_404(Product, pk=primary_key)
           data = ProductSerializer(obj, many=False).data
           return Response(data)     
       
       queryset = Product.objects.all()
       data = ProductSerializer(queryset, many=True).data 
       
       return Response(data)
         
    if method == "POST":
       serializer = ProductSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           title = serializer.validated_data.get('title')
           content = serializer.validated_data.get('content')

           if content is None:
               content = "content is none"
           serializer.save(content=content)
           return Response(serializer.data)
       return Response({"Error: Invalid data"}, status=400) 
