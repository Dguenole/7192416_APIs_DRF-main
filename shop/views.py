from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet    
from rest_framework.response import Response

from shop.models import Category
from shop.models import Product
from shop.models import Article
from shop.serializers import CategorySerializer
from shop.serializers import ProductSerializer
from shop.serializers import ArticleSerializer 


class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        queryset = Category.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id:
            queryset =queryset.filter(product_id=product_id)
        return queryset
    
    
class  ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset =  Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset =queryset.filter(category__id=category_id)
        return queryset
    
class  ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        queryset =  Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id:
            queryset =queryset.filter(product__id=product_id)
        return queryset


