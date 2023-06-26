"""
storage_csv.py - A module for CSV-based storage implementation of movie data.

This module provides a class, StorageCsv, which implements the IStorage interface and
allows storing and managing movie data in a CSV file. It utilizes the csv module for reading
and writing data to the CSV file.

Classes:
    StorageCsv: A storage implementation using a CSV file to store movie data.

Usage:
    1. Create an instance of StorageCsv by providing the file path to the CSV file.
    2. Use the provided methods to interact with the movie data:
        - list_movies(): Retrieve a dictionary of movies from the CSV file.
        - add_movie(title, year, rating, poster): Add a new movie to the CSV file.
        - delete_movie(title): Delete a movie from the CSV file.
        - update_movie(title, notes): Update the notes of a movie in the CSV file.
"""

import csv
from istorage import IStorage


class StorageCsv(IStorage):
    """
    A storage implementation using a CSV file to store movie data.

    The StorageCsv class provides methods to interact with a CSV file that stores movie information.
    It implements the IStorage interface, which defines the common storage methods.

    Args:
        file_path (str): The file path to the CSV file.

    Attributes:
        header (list[str]): The header of the CSV file, specifying the column names.
        file_path (str): The file path to the CSV file.
        data (list[dict]): The list of dictionaries representing movie data read from the CSV file.

    Methods:
        list_movies(): Retrieve a dictionary of movies from the CSV file.
        add_movie(title, year, rating, poster): Add a new movie to the CSV file.
        delete_movie(title): Delete a movie from the CSV file.
        update_movie(title, notes): Update the notes of a movie in the CSV file.

    """

    def __init__(self, file_path):
        """
        Initialize the StorageCsv instance.

        Args:
            file_path (str): The file path to the CSV file.

        """
        self.header = ['title', 'year', 'rating', 'poster', 'notes']
        self.file_path = file_path
        self.data = []

        # Read the existing data from the CSV file
        with open(self.file_path, "r", encoding="UTF-8", newline='') as fileobj:
            reader = csv.DictReader(fileobj, delimiter=",")
            for data in reader:
                self.data.append(data)

    def list_movies(self):
        """
        Retrieve a dictionary of movies from the CSV file.

        Returns:
            dict: A dictionary of movies with the movie title as the key
            and movie details as the value. Each movie detail is represented
            by a dictionary with keys 'year', 'rating', and 'poster'.

        """
        dictionary = {}
        for key in self.data:
            dictionary[key['title']] = {
                'year': key['year'],
                'rating': key['rating'],
                'poster': key['poster']
            }
        if not dictionary:
            return "Empty Database..."
        return dictionary

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the CSV file.

        Args:
            title (str): The title of the movie.
            year (str): The year of the movie.
            rating (str): The rating of the movie.
            poster (str): The poster URL of the movie.

        Returns:
            str: A message indicating the result of the operation.

        """
        movie_data = self.list_movies()
        if title in movie_data:
            return "Movie already exists"

        # Create a new movie dictionary
        movie = {
            'title': title,
            'year': year,
            'rating': rating,
            'poster': poster
        }

        # Add the movie to self.data
        self.data.append(movie)

        # Write the updated data to the CSV file
        with open(self.file_path, "w", encoding="UTF-8", newline='') as fileobj:
            writer = csv.DictWriter(fileobj, fieldnames=self.header)
            writer.writeheader()
            writer.writerows(self.data)

        return f"{title} added to the database"

    def delete_movie(self, title):
        """
        Delete a movie from the CSV file.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            str: A message indicating the result of the operation.

        """
        for movie in self.data:
            if title == movie['title']:
                self.data.remove(movie)
                with open(self.file_path, "w", encoding="UTF-8") as fileobj:
                    writer = csv.DictWriter(fileobj, fieldnames=self.header, delimiter=",")
                    writer.writeheader()
                    writer.writerows(self.data)
                return f"{title} has been deleted from the database"
        return f"{title} does not exist in the database"

    def update_movie(self, title, notes):
        """
        Update the notes of a movie in the CSV file.

        Args:
            title (str): The title of the movie to update.
            notes (str): The new notes to set for the movie.

        Returns:
            str: A message indicating the result of the operation.

        """
        for movie in self.data:
            if title == movie['title']:
                movie['notes'] = notes

        with open(self.file_path, "w", encoding="UTF-8", newline='') as fileobj:
            writer = csv.DictWriter(fileobj, fieldnames=self.header, delimiter=",")
            writer.writeheader()
            writer.writerows(self.data)

        if any(movie['title'] == title for movie in self.data):
            return f"{title} has been updated"
        return f"{title} does not exist"
