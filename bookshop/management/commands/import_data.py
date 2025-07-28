import sqlite3
import csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    @staticmethod
    def main():
        csv_file_path_genres = 'data/genres.csv'
        csv_file_path_authors = 'data/authors.csv'
        csv_file_path_books = 'data/books.csv'
        csv_file_path_books_genres = 'data/books_genres.csv'
        csv_file_path_admin = 'data/admin.csv'
        csv_file_path_agelimits = 'data/age_limits.csv'

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        with open(csv_file_path_genres, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                cursor.execute('''
                INSERT INTO bookshop_genre (name)
                VALUES (?)
                ''', (row[0],))

        with open(csv_file_path_authors, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                cursor.execute('''
                INSERT INTO bookshop_author (fullname)
                VALUES (?)
                ''', (row[0],))

        with open(csv_file_path_agelimits, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                cursor.execute('''
                INSERT INTO bookshop_agelimit (value)
                VALUES (?)
                ''', (row[0],))

        with open(csv_file_path_books, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                cursor.execute('''
                INSERT INTO bookshop_book (title, year, ISBN, age_limit_id, price, count, description, author_id, img_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],))

        with open(csv_file_path_books_genres, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                cursor.execute('''
                INSERT INTO bookshop_book_genres (book_id, genre_id)
                VALUES (?, ?)
                ''', (row[0], row[1],))

        with open(csv_file_path_admin, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                cursor.execute('''
                INSERT INTO auth_user (password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],))

        conn.commit()
        conn.close()

        print("Данные успешно импортированы")

    def handle(self, *args, **options):
        self.main()