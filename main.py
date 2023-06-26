"""
This script runs the movie application.

It imports the MovieApp class from the movie_app module and creates an instance of the MovieApp class
to run the movie application.

Usage:
    python main.py

"""

from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """
    Main function to run the movie application.

    It creates an instance of the MovieApp clas and calls the run() method to start the application.

    """
    storage = StorageCsv("movies.csv")
    jack = StorageJson("movies.json")
    jack_app = MovieApp(jack)
    movie_app = MovieApp(storage)
    print(movie_app.run())


if __name__ == "__main__":
    main()
