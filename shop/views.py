from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet    
from rest_framework.response import Response

from shop.models import Category
from shop.models import Product
from shop.serializers import CategorySerializer
from shop.serializers import ProductSerializer


class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.all()
    
class ProductView(APIView):
    def get(self,*args, **kwargs):
        queryset = Product.objects.all()
        seryalized = ProductSerializer(queryset, many=True)
        return Response(seryalized.data)
