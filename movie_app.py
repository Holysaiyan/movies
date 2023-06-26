"""
movie_app.py: A movie application that allows users to manage and interact with a movie database.

The Movie App provides various commands for users to perform operations on a movie database.
Users can list the movies in the database, add new movies, delete existing movies,
update movie notes, view movie statistics, get a random movie recommendation,
search for movies by keyword, generate a movie website, and sort movies by rating.

The application utilizes a `MovieStorage` class for storing and retrieving movie data.
The movie data includes movie titles, years, ratings, poster URLs, and notes.
The movie information is stored in a dictionary structure.

The `MovieApp` class serves as the main application logic, which interacts with the `MovieStorage`
class to perform database operations based on user commands. It provides a command-line interface
for users to input commands and view the output of each operation.

Usage:
    - Run the `movie_app.py` script to start the Movie App.
    - Follow the command prompts to interact with the movie database.
    - Enter the corresponding command number to perform a specific operation.
    - The output of each operation will be displayed on the console.

Author:
    Edikan Eshett

Date:
    23/06/2023
"""

import statistics
import random
from colorama import Fore, Style


class MovieApp:
    """
    A movie application class that manages movie storage and provides
    various commands to interact with the movies.
    """

    def __init__(self, movie_storage):
        self._storage = movie_storage

    def _command_list_movies(self):
        """
        Lists all the movies in the database.

        Returns:
            list: A list of dictionaries containing movie information (Title, Rating, Year).
                  Returns an empty list if no movies are present in the database.
        """
        movies = self._storage.list_movies()
        movies_list = []
        for title, info in movies.items():
            movie_info = {
                "Title": title,
                "Rating": info["rating"],
                "Year": info["year"]
            }
            movies_list.append(movie_info)
        return movies_list

    def _command_add_movie(self, movie_title, movie_year, movie_rating, movie_poster):
        """
        Adds a movie to the database.

        Args:
            movie_title (str): The title of the movie.
            movie_year (str): The year of the movie.
            movie_rating (float): The rating of the movie.
            movie_poster (str): The URL of the movie poster.

        Returns:
            str: A message indicating the success or failure of adding the movie.
        """
        return self._storage.add_movie(movie_title, movie_year, movie_rating, movie_poster)

    def _command_delete_movie(self, movie_title):
        """
        Deletes a movie from the database.

        Args:
            movie_title (str): The title of the movie to delete.

        Returns:
            str: A message indicating the success or failure of deleting the movie.
        """

        return self._storage.delete_movie(movie_title)

    def _command_update_movie(self, movie_title, movie_note):
        """
        Updates the note for a movie in the database.

        Args:
            movie_title (str): The title of the movie to update.
            movie_note (str): The new note for the movie.

        Returns:
            str: A message indicating the success or failure of updating the movie.
        """
        return self._storage.update_movie(movie_title, movie_note)

    def _command_movie_stats(self) -> str:
        """
        Returns the statistics of the movies in the database.

        Returns:
            str: A string containing the average rating,
                median rating, the best movie, and the worst movie.
        """
        movies = self._storage.list_movies()
        ratings = []
        for movie_data in movies.values():
            ratings.append(movie_data["rating"])

        # average
        average_rating = statistics.mean(ratings)
        result = f"Average rating: {average_rating}\n"

        # median
        median_rating = statistics.median(ratings)
        result += f"Median rating: {median_rating}\n"

        # best movie
        best_movie = max(ratings)
        for movie_title, movie_data in movies.items():
            if movie_data["rating"] == best_movie:
                result += f"The best movie: {Fore.GREEN}{movie_title}, " \
                          f"Rating: {best_movie}{Style.RESET_ALL}\n"

        # worst movie
        worst_movie = min(ratings)
        for movie_title, movie_data in movies.items():
            if movie_data["rating"] == worst_movie:
                result += f"The worst movie: {Fore.RED}{movie_title}, " \
                          f"Rating: {worst_movie}{Style.RESET_ALL}"

        return result

    def _command_random_movie(self):
        """
        Returns a randomly selected movie from the database.

        Returns:
            str or None: The title of a random movie, or None if the database is empty.
        """
        movie_data = self._storage.list_movies()
        if len(movie_data) == 0:
            return None

        random_title = random.choice(list(movie_data.keys()))
        return f"The movie for the night is '{random_title}'"

    def _command_search_movie(self, keyword):
        """
            Searches for movies in the database that match the provided keyword.

            Args:
                keyword (str): The keyword to search for in movie titles.

            Returns:
                list: A list of movie titles that match the keyword.
        """
        movie_data = self._storage.list_movies()
        matches = []
        for title in movie_data.keys():
            if keyword.lower() in title.lower():
                matches.append(title)
        return matches

    def _command_serialise_website(self, movie_data):
        """
        Serializes the movie data into HTML code for the website.

        Args:
            movie_data (dict): A dictionary where each key is a movie title,
                               and each value is a dictionary containing the movie's rating,
                               year, image URL, and note.

        Returns:
            str: HTML code representing the movie information for the website.
        """
        output = ''
        for movie_title, movie_info in movie_data.items():
            image_url = movie_info.get("image-url")
            if image_url:
                output += '<div class="movie">\n'
                output += f'<img class="movie-poster" src="{image_url}" alt="{movie_title}">\n'
                output += f'<h2 class="movie-title">{movie_title}</h2>\n'
                output += '<div class="movie-info">\n'
                output += f'<p class="movie-year">Year: {movie_info["year"]}</p>\n'
                if "note" in movie_info:
                    output += f'<p class="movie-note">{movie_info["note"]}</p>\n'
                output += '</div>\n'
                output += '</div>\n'
        return output

    def _command_generate_website(self):
        """
        Generates the movie website.

        The function reads the website template file, replaces the placeholders
        with the serialized movie information,and saves the generated website to a file.
        """
        with open("index_template.html", "r", encoding="utf-8") as fileobj:
            data = fileobj.read()
            serialised_data = self._command_serialise_website \
                (self._storage.list_movies())
            html_replace_title = data.replace("__TEMPLATE_TITLE__", "My Movie App")
            html_template_and_data_replace_text = html_replace_title. \
                replace("__TEMPLATE_MOVIE_GRID__", serialised_data)

        with open("website.html", "w", encoding="utf-8") as file:
            file.write(html_template_and_data_replace_text)

        return "Website has been generated"

    def _command_sort_movies(self) -> str:
        """
        Sorts the movies from the lowest rating to the highest rating.

        Returns:
            str: A string containing the sorted movies with their ratings.
        """
        movie_data = self._storage.list_movies()
        sorted_movies = sorted(movie_data.items(), key=lambda item: item[1]['rating'])

        result = ""
        for movie_title, values in sorted_movies:
            result += f"Movie: {movie_title}, Rating: {values['rating']}\n"

        return result

    def help_menu(self):
        """
        Prints out the help message for all the commands of the program.
        """
        print("____COMMAND LIST_____")
        print("1. List Movies")
        print("2. Add Movie")
        print("3. Delete Movie")
        print("4. Update Movie")
        print("5. Movie Statistics")
        print("6. Random Movie")
        print("7. Movie Search")
        print("8. Generate Website")
        print("9. Sort movies")
        print("10. Exit program")

    def execute_command(self, command):
        """
        Executes the given command.

        Args:
            command (str): The command to execute.

        Returns:
            str: The output message of the command execution.
        """
        if command == "1":
            movie_result = ""
            movies = self._command_list_movies()
            if movies:
                for movie in movies:
                    movie_result += f"Title: {movie['Title']}\n"
                    movie_result += f"Rating: {movie['Rating']}\n"
                    movie_result += f"Year: {movie['Year']}\n\n"
                return movie_result
            return "No movies in the database."

        elif command == "2":
            movie_title = input("Enter Movie Title: ")
            movie_year = input("Enter Movie Year: ")
            movie_rating = float(input("Enter movie rating: "))
            movie_poster = input("Enter poster url: ")
            result = self._command_add_movie(movie_title, movie_year, movie_rating, movie_poster)
            return result

        elif command == "3":
            movie_title = input("Enter movie Title: ")
            result = self._command_delete_movie(movie_title)
            return result

        elif command == "4":
            movie_title = input("Enter movie Title: ")
            movie_note = input("Enter movie note: ")
            result = self._command_update_movie(movie_title, movie_note)
            return result

        elif command == "5":
            result = self._command_movie_stats()
            return result

        elif command == "6":
            result = self._command_random_movie()
            return result

        elif command == "7":
            keyword = input("Enter a keyword to search: ")
            search_result = self._command_search_movie(keyword)
            if search_result:
                print("Search Results:")
                for result in search_result:
                    print(f"{result}")

        elif command == "8":
            result = self._command_generate_website()
            return result

        elif command == "9":
            result = self._command_sort_movies()
            return result

        elif command == "10":
            return "Exiting the program"

        else:
            return "Invalid command. Please try again."

    def run(self):
        """
        Runs the movie application.
        """
        print("Welcome to the Movie App!")
        while True:
            self.help_menu()
            command = input("Enter a command (1-10): ")
            result = self.execute_command(command)
            print(result)
            if command == "10":
                break
