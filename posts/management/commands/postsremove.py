from django.core.management.base import BaseCommand, CommandError
from posts.models import Category, Post

class Command(BaseCommand):
    help = 'Remove posts by category'

    requires_migrations_checks = True
    missing_args_message = 'Not enough arguments'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you really want to delete posts {options["category"]}? yes/no: ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Canceled'))
            return

        try:
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all posts form category {category.category_name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.category_name}'))