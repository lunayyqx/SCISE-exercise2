import sqlite3

def create_database_and_table():
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
            movieID INTEGER PRIMARY KEY,
            movieName TEXT,
            movieYear INTEGER,
            imdbRating REAL
        )
    ''')
    conn.commit()
    conn.close()

def populate_database_from_file(file_name):
    try:
        conn = sqlite3.connect("stephen_king_adaptations.db")
        cursor = conn.cursor()
        
        with open(file_name, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 4:
                    cursor.execute('''
                        INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
                        VALUES (?, ?, ?)
                    ''', (data[0], int(data[1]), float(data[3])))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def search_movies():
    while True:
        print("Search options:")
        print("1. Movie name")
        print("2. Movie year")
        print("3. Movie rating")
        print("4. STOP")
        option = input("Choose an option: ")
        
        if option == "1":
            movie_name = input("Enter the name of the movie: ")
            search_movie_by_name(movie_name)
        elif option == "2":
            year = input("Enter the year: ")
            search_movies_by_year(year)
        elif option == "3":
            rating = input("Enter the minimum rating: ")
            search_movies_by_rating(rating)
        elif option == "4":
            break
        else:
            print("Invalid option. Please choose a valid option.")

def search_movie_by_name(movie_name):
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM stephen_king_adaptations_table
        WHERE movieName = ?
    ''', (movie_name,))
    movie = cursor.fetchone()
    conn.close()
    
    if movie:
        print_movie_details(movie)
    else:
        print("No such movie exists in our database.")

def search_movies_by_year(year):
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM stephen_king_adaptations_table
        WHERE movieYear = ?
    ''', (year,))
    movies = cursor.fetchall()
    conn.close()
    
    if movies:
        print("Movies released in", year)
        for movie in movies:
            print_movie_details(movie)
    else:
        print(f"No movies were found for the year {year} in our database.")

def search_movies_by_rating(min_rating):
    conn = sqlite3.connect("stephen_king_adaptations.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM stephen_king_adaptations_table
        WHERE imdbRating >= ?
    ''', (min_rating,))
    movies = cursor.fetchall()
    conn.close()
    
    if movies:
        print("Movies with IMDb rating of", min_rating, "or higher:")
        for movie in movies:
            print_movie_details(movie)
    else:
        print(f"No movies at or above {min_rating} rating were found in the database.")

def print_movie_details(movie):
    print("Movie ID:", movie[0])
    print("Movie Name:", movie[1])
    print("Movie Year:", movie[2])
    print("IMDb Rating:", movie[3])

if __name__ == "__main__":
    create_database_and_table()
    populate_database_from_file("stephen_king_adaptations.txt")
    search_movies()