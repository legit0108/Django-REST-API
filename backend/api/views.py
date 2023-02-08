from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer

# Create your views here.

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    data = request.data

    serializer = ProductSerializer(data=data)
    
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        return Response(serializer.data)
    return Response({"Error: Invalid data"}, status=400)