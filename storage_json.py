"""
Module: storage_json

This module provides the StorageJson class for storing and managing movie data in a JSON file.

Classes:
    StorageJson: A storage implementation using a JSON file to store movie data.

Usage:
    1. Create an instance of StorageJson by providing the file path to the JSON file.
    2. Use the provided methods to interact with the movie data:
        - list_movies(): Retrieve the list of movies from the JSON file.
        - add_movie(title, year, rating, poster): Add a new movie to the JSON file.
        - delete_movie(title): Delete a movie from the JSON file.
        - update_movie(title, notes): Update the notes of a movie in the JSON file.

Example:
    from storage_json import StorageJson

    # Create an instance of StorageJson
    storage = StorageJson('movies.json')

    # Add a new movie
    storage.add_movie('Avatar', 2009, 7.8, 'https://example.com/avatar-poster.jpg')

    # List all movies
    movies = storage.list_movies()
    for movie in movies:
        print(f"Title: {movie['title']}")
        print(f"Year: {movie['year']}")
        print(f"Rating: {movie['rating']}")
        print(f"Poster: {movie['poster']}")
        print()

Note:
    - The JSON file must contain a dictionary with movie titles as keys and movie details
      (year, rating, poster) as values.
    - The file is read and overwritten when the StorageJson instance is initialized.
    - The 'add_movie', 'delete_movie', and 'update_movie' methods modify the JSON file
      directly.

"""

import json
from istorage import IStorage


class StorageJson(IStorage):
    """
    StorageJson class implements the IStorage interface for storing movie data in a JSON file.

    Attributes:
        year (int): The year of the movie.
        title (str): The title of the movie.
        rating (float): The rating of the movie.
        poster (str): The URL of the movie poster.
        file_path (str): The path to the JSON file.

    Methods:
        list_movies(): Returns the list of movies.
        add_movie(title, year, rating, poster): Adds a new movie to the database.
        delete_movie(title): Deletes a movie from the database.
        update_movie(title, notes): Updates the notes of a movie in the database.
    """

    def __init__(self, file_path):
        """
        Initialize the StorageJson instance.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path
        with open(self.file_path, "r", encoding="utf-8") as fileobj:
            self.data = json.load(fileobj)

    def list_movies(self):
        """
        Retrieve the list of movies from the JSON file.

        Returns:
            dict: A dictionary containing the movie data.
        """
        return self.data

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the database.

        Args:
            title (str): The title of the movie.
            year (int): The year of the movie.
            rating (float): The rating of the movie.
            poster (str): The URL of the movie poster.

        Returns:
            str: A message indicating the status of the operation.
        """
        if title in self.data:
            return "Movie already exists"

        self.data[title] = {
            'year': year,
            'rating': rating,
            'image-url': poster
        }

        with open(self.file_path, "w", encoding="utf-8") as fileobj:
            json.dump(self.data, fileobj)

        return f"{title} has been added to the database"

    def delete_movie(self, title):
        """
        Deletes a movie from the database.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            str: A message indicating the status of the operation.
        """
        for movie_title in self.data:
            if title.lower() == movie_title.lower():
                del self.data[movie_title]
                with open(self.file_path, "w", encoding="utf-8") as fileobj:
                    json.dump(self.data, fileobj)
                return f"{title} has been deleted from the database"
        return f"{title} does not exist in the database"

    def update_movie(self, title, notes):
        """
        Updates the notes of a movie in the database.

        Args:
            title (str): The title of the movie to update.
            notes (str): The new notes to assign to the movie.

        Returns:
            str: A message indicating the status of the operation.
        """
        movie_database = self.data

        for movie_title, values in movie_database.items():
            if title.lower() == movie_title.lower() and 'image-url' in values:
                self.data[movie_title]['note'] = notes
                with open(self.file_path, "w", encoding="utf-8") as fileobj:
                    json.dump(self.data, fileobj)
                return f"Note added to the movie '{movie_title}' successfully. Now try to hover over the movie"
        return "Movie does not exist or does not have an 'image-url' field."
