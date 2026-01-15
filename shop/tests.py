from django.urls import reverse_lazy 
from rest_framework.test import APITestCase
from shop.models import Category, Product, Article  


class TestCategoryAPI(APITestCase):

    url = reverse_lazy('category-list') 

    def format_datetime(self, value):
        return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    def test_list(self):
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='légumes', active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                'id': category.id,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
                'name': category.name
            },
        ]
        self.assertEqual(response.json(), expected)