from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase
from shop.models import Category, Product, Article  


class ShopAPITestCase(APITestCase):
    
    def format_datetime(self, value):
        return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


class TestCategoryAPI(ShopAPITestCase):

    url = reverse_lazy('category-list')
    
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

    def test_create(self):
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Tentative'})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.exists())


class TestProductAPI(ShopAPITestCase):

    url = reverse_lazy('product-list')
    
    def test_list(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)
        Product.objects.create(name='Kiwi', category=category, active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                'id': product.id,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'name': product.name,
                'category': category.id
            },
        ]
        self.assertEqual(response.json(), expected)

    def test_detail(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)

        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'id': product.id,
            'date_created': self.format_datetime(product.date_created),
            'date_updated': self.format_datetime(product.date_updated),
            'name': product.name,
            'category': category.id
        }
        self.assertEqual(response.json(), expected)

    def test_list_filter_by_category(self):
        category1 = Category.objects.create(name='Fruits', active=True)
        category2 = Category.objects.create(name='Légumes', active=True)
        product1 = Product.objects.create(name='Banane', category=category1, active=True)
        Product.objects.create(name='Courgette', category=category2, active=True)

        url = f'{self.url}?category_id={category1.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], product1.id)

    def test_create(self):
        category = Category.objects.create(name='Fruits', active=True)
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.url, data={'name': 'Tentative', 'category': category.id})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Product.objects.exists())

    def test_update(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.put(url, data={'name': 'Tentative de modification', 'category': category.id})
        self.assertEqual(response.status_code, 405)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Banane')

    def test_delete(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Product.objects.exists())