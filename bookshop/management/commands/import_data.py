import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from bookshop.models import Book, AgeLimit, Author, Genre


class Command(BaseCommand):
    @staticmethod
    @transaction.atomic
    def main():
        CSV_FILE_PATH_GENRES = 'data/genres.csv'
        CSV_FILE_PATH_AUTHORS = 'data/authors.csv'
        CSV_FILE_PATH_BOOKS = 'data/books.csv'
        CSV_FILE_PATH_BOOKS_GENRES = 'data/books_genres.csv'
        CSV_FILE_PATH_AGELIMITS = 'data/age_limits.csv'

        with open(CSV_FILE_PATH_AGELIMITS, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                AgeLimit.objects.get_or_create(
                    id=row[0],
                    defaults={"value": row[1]},
                )

        print("Возрастные ограничения загружены")
        
        with open(CSV_FILE_PATH_AUTHORS, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                Author.objects.get_or_create(
                    id=row[0],
                    defaults={"fullname": row[1]},
                )
        print("Авторы загружены")

        with open(CSV_FILE_PATH_GENRES, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                Genre.objects.get_or_create(
                    id=row[0],
                    defaults={"name": row[1]},
                )
        print("Жанры загружены")

        with open(CSV_FILE_PATH_BOOKS, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                age_limit = AgeLimit.objects.filter(id=row[4]).first()
                author = Author.objects.filter(id=row[8]).first()
                Book.objects.get_or_create(
                    id=row[0],
                    defaults={
                        "title": row[1],
                        "year": row[2],
                        "ISBN": row[3],
                        "age_limit": age_limit,
                        "price": row[5],
                        "count": row[6],
                        "description": row[7],
                        "author": author,
                        "img_path": row[9],
                    },
                )
        print("Книги загружены")

        with open(CSV_FILE_PATH_BOOKS_GENRES, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            objs = []
            Through = Book.genres.through
            for row in csvreader:
                book_id, genre_id = row[1], row[2]

                objs.append(Through(id=row[0], book_id=book_id, genre_id=genre_id))

            Through.objects.bulk_create(objs, ignore_conflicts=True)
        print("Связи книги-жанры загружены")

        print("Данные успешно импортированы")

    def handle(self, *args, **options):
        self.main()