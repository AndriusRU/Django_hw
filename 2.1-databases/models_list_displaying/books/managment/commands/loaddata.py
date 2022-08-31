import json

from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_arguments('filename', type=str, help="Enter file name")

    def handle(self, *args, **options):
        filename = options['filename']

        with open(filename, 'r') as file:
            books = json.load(file)

        for book in books:

            Book.objects.create(
                name=book.get('fields').get('name'),
                author=book.get('fields').get('author'),
                pub_date=book.get('fields').get('pub_date'),
            )
