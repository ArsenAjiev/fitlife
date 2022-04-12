from membership.models import Subscription
from django.core.management.base import BaseCommand
from django.db.utils import Error


class Command(BaseCommand):
    help = 'Create category for DB'

    def handle(self, *args, **kwargs):
        list_category = ['4t', '8t', '12t']
        for i in list_category:
            try:
                subscription = Subscription.objects.create(title=i, price=20, description='description')
            except Error:
                print('subscription "%s" exist' % i)
                continue
            self.stdout.write(self.style.SUCCESS('Successfully created "%s" subscription' % subscription))