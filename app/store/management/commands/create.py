from store.models import Product
from django.core.management.base import BaseCommand
from django.db.utils import Error


class Command(BaseCommand):
    help = 'Create category for DB'

    def handle(self, *args, **kwargs):
        list_category = ['Headphones', 'Mount of Olives Book', 'Project Sourse Code', 'Watch', 'Shoes', 'T-Shirt']
        for i in list_category:
            try:
                product = Product.objects.create(name=i, price=14.99)
            except Error:
                print('Category "%s" exist' % i)
                continue
            self.stdout.write(self.style.SUCCESS('Successfully created "%s" category' % product))