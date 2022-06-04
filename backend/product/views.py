import json
from re import L
from django.http import Http404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics

from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer, CategoryListSerializer, ProductSerializerCrud

### Product ###
class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AllProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCount(APIView):
    def get(self, request, format=None):
        products = Product.objects.count()
        return Response(products)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductByUuid(APIView):
    def get(self, request, uuid_slug):
        product = Product.objects.get(uuid=uuid_slug)
        serializer = ProductSerializerCrud(product)
        return Response(serializer.data)

class AddProduct(APIView):
    def post(self, request, format=None):
        serializer = ProductSerializerCrud(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UpdateProduct(generics.UpdateAPIView):
    def put(self, request, format=None, *args, **kwargs):
        product = Product.objects.get(uuid = request.data['uuid'])
        serializer = ProductSerializerCrud(instance=product, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(status.HTTP_400_BAD_REQUEST)

class DeleteProduct(APIView):
    def delete(self, request, uuid_slug, format=None):
        product = Product.objects.get(uuid=uuid_slug)
        product.delete()
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response([])

### Category ###        
class AllCategoryList(APIView):
    def get(self, reqeust, format=None):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class AddCategory(APIView):
    def post(self, request, format=None):
        serializer = CategoryListSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UpdateCategory(APIView):
    def put(self, request, format=None):
        category = Category.objects.get(id=request.data['id'])
        serializer = CategoryListSerializer(instance=category, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)

class DeleteCategory(APIView):
    def delete(self, request, id_slug, format=None):
        category = Category.objects.get(id=id_slug)
        category.delete()
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
